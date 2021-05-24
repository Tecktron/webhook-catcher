from django.db import models
from django_postgres_unlimited_varchar import UnlimitedCharField


class WebhookData(models.Model):
    method = models.CharField("HTTP Method", max_length=56)
    path = UnlimitedCharField("Incoming path")
    params = models.JSONField("Query params", null=True)
    json = models.JSONField("Json data", null=True)
    data = models.TextField("Raw data")
    headers = models.JSONField("Request headers")
    created = models.DateTimeField("Time created", auto_now_add=True)

    class Meta:
        verbose_name = "Webhook Data"
        verbose_name_plural = "Webhooks Data"
