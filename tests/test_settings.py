from webhook_catcher.settings import *  # noqa: F403

DEBUG = True
ENVIRONMENT = "test"

LOGGING = {"version": 1, "loggers": []}

TEMPLATES[0]["OPTIONS"]["debug"] = True  # noqa: F405

TEST_DATABASE_PREFIX = "test_"

SECURE_SSL_REDIRECT = False

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache", "KEY_PREFIX": "testing-dummy-key"}}

TIME_ZONE = "UTC"
