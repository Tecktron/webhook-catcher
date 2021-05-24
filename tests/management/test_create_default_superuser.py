from io import StringIO

import pytest
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


@pytest.mark.django_db
def create_default_superuser_test():
    """Test creating a default super user"""
    username = "admin"
    password = "12345"

    args = []
    opts = {"username": username, "password": password}
    from django.core.management import call_command

    call_command("create_default_superuser", *args, **opts)
    admin = User.objects.filter(username=username).first()
    assert admin.username == username
    assert check_password(password, admin.password) is True
    assert admin.is_superuser is True
    out = StringIO()
    call_command("create_default_superuser", *args, stdout=out, **opts)
    assert out.getvalue().strip() == f"User {username} already exists"
