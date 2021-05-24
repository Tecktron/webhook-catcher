import freezegun
import pytest
from django.contrib import admin
from tests.factories import WebhookData, WebhookDataFactory

from webhook_catcher.admin import WebhookDataAdmin


@pytest.mark.django_db
class AdminTests:
    """Test the Admin view's customized functions"""

    @pytest.fixture(autouse=True)
    @freezegun.freeze_time("2021-04-20")
    def setup(self, admin_client, mocker):
        self.model = WebhookDataFactory()
        self.admin_cls = WebhookDataAdmin(WebhookData, admin.site)
        self.mocker = mocker
        self.admin_client = admin_client

    def test_time(self):
        output = self.admin_cls.time(self.model)
        assert output == "04/20/21 12:00:00am"

    def test_page(self):
        response = self.admin_client.get("/admin/webhook_catcher/webhookdata/")
        assert response.status_code == 200

    def test_get_fields(self):
        fields = self.admin_cls.get_fields(request=None, obj=None)
        assert fields == []

        fields = self.admin_cls.get_fields(request=None, obj=self.model)
        assert fields == ["time", "method", "path", "json", "headers"]

        self.model.params = "stuff"
        fields = self.admin_cls.get_fields(request=None, obj=self.model)
        assert fields == ["time", "method", "path", "params", "json", "headers"]

        self.model.json = None
        fields = self.admin_cls.get_fields(request=None, obj=self.model)
        assert fields == ["time", "method", "path", "params", "data", "headers"]

    def test_changeform_view(self):
        mocked_super_fn = self.mocker.patch("webhook_catcher.admin.ModelAdmin.changeform_view")
        mocked_super_fn.return_value = None
        admin_cls = WebhookDataAdmin(WebhookData, admin.site)
        admin_cls.changeform_view(None)
        assert mocked_super_fn.called is True
        assert mocked_super_fn.call_args.kwargs["extra_context"] == {
            "show_save_and_continue": False,
            "show_save": False,
            "show_save_and_add_another": False,
            "show_delete_link": False,
        }

    @pytest.mark.parametrize(
        ("function", "param_count"),
        (
            ("has_add_permission", 1),
            ("has_delete_permission", 2),
            ("save_model", 4),
            ("delete_model", 2),
            ("save_related", 4),
        ),
    )
    def test_functions_return_false(self, function, param_count):
        value = getattr(self.admin_cls, function)(*[None for i in range(param_count)])
        assert value is False
