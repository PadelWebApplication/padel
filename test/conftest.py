import pytest
from unittest.mock import patch

from base.models import Session, Service
from client.models import Client
from coach.models import Coach
from userauths.models import User

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@mail.com',
        password='Test@pass183810jdf_'
    )


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        email='client@mail.com', password='Test@pass183810jdf_'
    )


@pytest.fixture
def client(client_user):
    return Client.objects.create(user=client_user)


@pytest.fixture
def coach(coach_user):
    return Coach.objects.create(user=coach_user)


@pytest.fixture
def coach_user(db):
    return User.objects.create_user(
        email='coach@mail.com', password='Test@pass183810jdf_'
    )


@pytest.fixture
def session(db, service, client, coach):
    return Session.objects.create(
        service=service,
        coach=coach,
        client=client
    )


@pytest.fixture
def service(db):
    return Service.objects.create(name='Test service', cost=10)


@pytest.fixture
def mock_user_id():
    def _mock(user_id):
        return patch(
            'core.middleware.AccessLogMiddleware.get_current_user_id',
            return_value=user_id
        )
    return _mock
