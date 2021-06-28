from django.conf import settings
from django.db import transaction
from functools import wraps
import models_common
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_filters.backends import DjangoFilterBackend


def custom_update(self, request, *args, **kwargs):
    """Update method overridden to save the cur_saved_instance(clone), to itself, for further reference,
    e.g. in places like
    * Notification generation
    * clean routines
    * etc
    """
    partial = kwargs.pop("partial", False)
    instance = self.get_object()
    if isinstance(instance, models_common.ExchangeBaseModel):
        setattr(instance, "cur_saved_instance", instance.clone())
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)

    if getattr(instance, "_prefetched_objects_cache", None):
        # If 'prefetch_related' has been applied to a queryset, we need to
        # forcibly invalidate the prefetch cache on the instance.
        instance._prefetched_objects_cache = {}

    return Response(serializer.data)


def custom_dispatch(self, request, *args, **kwargs):
    """
    `.dispatch()` is pretty much the same as Django's regular dispatch,
    but with extra hooks for startup, finalize, and exception handling.
    """
    self.args = args
    self.kwargs = kwargs
    request = self.initialize_request(request, *args, **kwargs)
    self.request = request
    self.headers = self.default_response_headers  # deprecate?

    try:
        self.initial(request, *args, **kwargs)

        # Get the appropriate handler method
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed,
            )
        else:
            handler = self.http_method_not_allowed

        # overridden block to handle atomic requests based on view level configuration
        database_config = settings.DATABASES['default']
        if not (
                "ATOMIC_REQUESTS" in database_config and database_config["ATOMIC_REQUESTS"]
        ) and (
                getattr(self, "ATOMIC_REQUESTS", False)
                or getattr(handler, "ATOMIC_REQUESTS", False)
        ):
            with transaction.atomic(using="default"):
                response = handler(request, *args, **kwargs)
        else:
            response = handler(request, *args, **kwargs)

    except Exception as exc:
        response = self.handle_exception(exc)

    self.response = self.finalize_response(request, response, *args, **kwargs)
    return self.response


def get_base_viewset(
        create=True, read=True, list=True, update=True, delete=True,
):
    classes = {
        "create": viewsets.mixins.CreateModelMixin,
        "read": viewsets.mixins.RetrieveModelMixin,
        "list": viewsets.mixins.ListModelMixin,
        "update": viewsets.mixins.UpdateModelMixin,
        "delete": viewsets.mixins.DestroyModelMixin,
    }
    inheritance_classes = []
    for each in tuple(locals().keys()):
        if each in classes and locals()[each] is True:
            inheritance_classes.append(classes[each])

    inheritance_classes.append(viewsets.GenericViewSet)

    klass = type(
        "ViewSetClass",
        tuple(inheritance_classes),
        {
            "search_fields": tuple(),
            "filter_backends": (DjangoFilterBackend, OrderingFilter, SearchFilter),
            "lookup_value_regex": r"\d+",
        },
    )

    if update is True:
        klass.update = custom_update

    klass.dispatch = custom_dispatch

    return klass


ExchangeModelViewSet = get_base_viewset()
ExchangeReadOnlyModelViewSet = get_base_viewset(create=False, delete=False, update=False)
ExchangeGenericViewSet = get_base_viewset(
    create=False, delete=False, update=False, read=False,
)
ExchangeReadUpdateViewSet = get_base_viewset(create=False, delete=False)


def transaction_atomic_db(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    setattr(inner, "ATOMIC_REQUESTS", True)
    return inner
