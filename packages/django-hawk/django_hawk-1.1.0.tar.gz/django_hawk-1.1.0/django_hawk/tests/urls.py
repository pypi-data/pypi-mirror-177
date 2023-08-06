from django.urls import path

from django_hawk.tests.views import simple_view

urlpatterns = [
    path(
        "test-simple-view/",
        simple_view,
        name="test_simple_view",
    ),
]
