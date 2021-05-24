from django.contrib.admin import ModelAdmin, register
from django.db.models.fields.json import JSONField
from prettyjson import PrettyJSONWidget

from webhook_catcher.models import WebhookData


@register(WebhookData)
class WebhookDataAdmin(ModelAdmin):
    search_fields = ("path",)
    empty_value_display = "Null"
    list_filter = ("method",)
    list_display = ("time", "method", "path")
    readonly_fields = ("time", "method", "path")
    formfield_overrides = {
        JSONField: {"widget": PrettyJSONWidget(attrs={"initial": "parsed"})},
    }

    @staticmethod
    def time(obj):
        return obj.created.strftime("%x %I:%M:%M%P").lower()

    def get_fields(self, request, obj=None):
        if not obj:
            return []
        fields = ["time", "method", "path"]
        if obj.params:
            fields.append("params")
        if obj.json:
            fields.append("json")
        elif obj.data:
            fields.append("data")
        fields.append("headers")
        return fields

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context["show_save_and_continue"] = False
        extra_context["show_save"] = False
        extra_context["show_save_and_add_another"] = False
        extra_context["show_delete_link"] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        return False

    def delete_model(self, request, obj):
        return False

    def save_related(self, request, form, formsets, change):
        return False
