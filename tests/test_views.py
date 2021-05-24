import json

import pytest
from django.template.loader import render_to_string

from webhook_catcher.models import WebhookData
from webhook_catcher.views import CatcherView


def test_no_favicon(rf):
    """Ensure favicon gives a 404"""
    request = rf.get("favicon.ico")
    response = CatcherView.as_view()(request)
    assert response.status_code == 404


def test_index_view(rf):
    """Ensure the index view is shown when requested"""
    request = rf.get("/")
    response = CatcherView.as_view()(request)
    assert response.status_code == 200
    assert response.content == render_to_string("index.html").encode("utf-8")


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("method", "path", "content", "content_type", "response_code"),
    (
        # NOTE: Since we use the Django request factory, we are limited to the methods it supports
        ("POST", "/test/post", json.dumps({"test": "json data"}), "application/json", 204),
        ("POST", "", "<p>Some HTML text</p>", "text/html", 204),
        ("PUT", "/test/put", json.dumps({"test": "json data"}), "application/json", 204),
        ("PUT", "/test/fail-json", "Not Json", "application/json", 400),
        ("GET", "/test", "", "", 204),
    ),
)
def test_catcher_view(method, path, content, content_type, response_code, rf):
    """Test to Ensure that the data is caught and saved"""
    method_type = method.lower()
    if method_type == "get":
        request = rf.get(path, content)
    else:
        request = getattr(rf, method.lower())(path, data=content, content_type=content_type)

    response = CatcherView.as_view()(request)
    assert response.status_code == response_code

    instance = WebhookData.objects.last()
    assert instance.path == path if path else "/"
    assert instance.data == content
    assert instance.method == method
    assert instance.headers.get("Content-Type", "") == content_type
    if content_type == "application/json" and response_code == 204:
        assert json.dumps(instance.json) == content
    else:
        assert instance.json is None
