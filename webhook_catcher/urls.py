from django.contrib import admin
from django.urls import path

from webhook_catcher.views import CatcherView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("<path:_>", CatcherView.as_view()),
    path("", CatcherView.as_view()),
]
