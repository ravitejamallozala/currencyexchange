from rest_framework.test import APIClient
import rest_framework.status
from django.core.urlresolvers import reverse

from settings import UNITTEST_HTTP_HOST


class CommonTestCasesMixin(object):
    """ Define class variables url, data, invalid_data in whichever class extends this."""

    def test_no_authentication(self):
        """ Expect Authentication error message when there is no token """
        client = APIClient()
        client.credentials(HTTP_HOST=UNITTEST_HTTP_HOST)
        response = client.get(reverse(self.name + "-list"))
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            response.json()["detail"], "Authentication credentials were not provided.",
        )

    def test_invalid_token(self):
        """ Expect Authentication error message when there is invalid token """
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + "#asjdfljasldf", HTTP_HOST=UNITTEST_HTTP_HOST,
        )
        response = client.get(reverse(self.name + "-list"))
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(response.json()["detail"], "Invalid token.")

    def test_valid_token(self):
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + self.access_token,
            HTTP_HOST=UNITTEST_HTTP_HOST,
        )
        response = client.get(reverse(self.name + "-list"))
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)

    def test_invalid_input(self):
        """
        Expect status code of 400 for invalid input
        All the parameters passed should be invalid.
        """
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + self.access_token,
            HTTP_HOST=UNITTEST_HTTP_HOST,
        )
        response = client.post(
            reverse(self.name + "-list"), self.invalid_data, format="json",
        )
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_400_BAD_REQUEST,
        )
        # for name in self.invalid_data_fields:
        #     self.assertIn(name, response.json())

    def test_create(self):
        """ Expect 201 response status """
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + self.access_token,
            HTTP_HOST=UNITTEST_HTTP_HOST,
        )
        response = client.post(reverse(self.name + "-list"), self.data, format="json")
        print(reverse(self.name + "-list"), "----------------->", response.data)
        self.assertEqual(response.status_code, rest_framework.status.HTTP_201_CREATED)
        for name, value in list(self.data.items()):
            if not (name.endswith("_id") or name.endswith("_ids")):
                final_value = (
                    self.result_display_data.get(name, value)
                    if hasattr(self, "result_display_data")
                    else value
                )
                # self.assertEqual(final_value, response.json()[name])
        return response.json()

    def test_put(self):
        """ Expect 200 response status and valid data changed """
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + self.access_token,
            HTTP_HOST=UNITTEST_HTTP_HOST,
        )
        new_item = self.test_create()
        modify_item = {}

        # Copy over the fields from the new_item to the modify_item;
        # replace foreignkey values (which will be dictionaries) by just their 'id' field
        for k, v in list(new_item.items()):
            if hasattr(self, "put_exempt_keys") and (k in self.put_exempt_keys):
                continue
            if type(v) == dict:
                modify_item["{}_id".format(k)] = v["id"]
            else:
                modify_item[k] = (
                    self.data.get(k, v) if hasattr(self, "result_display_data") else v
                )

        response = client.put(
            reverse(self.name + "-detail", kwargs={"pk": modify_item["id"]}),
            modify_item,
            format="json",
        )
        self.assertEqual(response.status_code, rest_framework.status.HTTP_200_OK)

        response_item = response.json().copy()
        del new_item["modified"]
        del response_item["modified"]

        self.assertEqual(new_item, response_item)
        return response.json()

    def test_delete(self):
        """ Expect 200 response status and valid data changed """
        client = APIClient()
        client.credentials(
            HTTP_AUTHORIZATION="Token " + self.access_token,
            HTTP_HOST=UNITTEST_HTTP_HOST,
        )
        new_item = self.test_create()
        response = client.delete(
            reverse(self.name + "-detail", kwargs={"pk": new_item["id"]}),
            {},
            format="json",
        )
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_204_NO_CONTENT,
        )
