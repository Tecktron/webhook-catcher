import json
import logging

from django.http.response import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
)
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from webhook_catchall.models import WebhookData

logger = logging.getLogger(__name__)


class CatchAllView(View):
    @staticmethod
    def get_index():
        content = render_to_string("index.html")
        return HttpResponse(content, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.path.endswith("favicon.ico"):
            return HttpResponseNotFound(content=b"Not Found")
        if request.method == "GET" and request.path in {"", "/"}:
            return self.get_index()

        caught_webhook = WebhookData(
            path=request.path,
            method=request.method,
            params=dict(request.GET.lists()),
            headers=dict(request.headers),
            data=request.body.decode("utf-8"),
        )
        content_type = request.META.get("CONTENT_TYPE", "text/plain")
        error_reason = None
        if "application/json" in content_type and len(request.body) > 0:
            try:
                json_data = json.loads(request.body)
                caught_webhook.json = json_data
            except (TypeError, json.JSONDecodeError) as e:
                error_reason = f"Invalid JSON Input. Error: {e}"
                logger.warning(error_reason)

        caught_webhook.save()
        return (
            HttpResponse(status=204)
            if not error_reason
            else HttpResponseBadRequest(error_reason)
        )
