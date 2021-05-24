from datetime import timezone

import factory

from webhook_catcher.models import WebhookData


class WebhookDataFactory(factory.django.DjangoModelFactory):
    method = factory.Faker("random_element", elements={"POST", "PUT"})
    path = factory.Faker("uri_path")
    params = None
    json = factory.Faker("json", data_columns={"id": "pyint", "name": "word", "description": "bs"}, num_rows=1)
    data = factory.lazy_attribute(lambda o: str(o.json))
    headers = {"Content-Type": "application/json"}
    created = factory.Faker("date_time", tzinfo=timezone.utc)

    class Meta:
        model = WebhookData
