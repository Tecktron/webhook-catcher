import json
import logging

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from webhook_catchall.models import WebhookData

logger = logging.getLogger(__name__)


class CatchAllView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.path.endswith("favicon.ico"):
            return HttpResponseNotFound(content="Not Found")
        if request.path.startswith("/admin/") or request.path.startswith("/static/"):
            return super().dispatch(request, *args, **kwargs)

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
