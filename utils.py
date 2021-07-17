from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.request import Request

def get_restframework_request(url, body):
    req = RequestFactory(content_type="application/json")
    req = req.post(url, content_type="application/json", data=body)
    req = Request(req)
    req.session = {}
    session_obj = SessionMiddleware()
    session_obj.process_request(req)
    return req
