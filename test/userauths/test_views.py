import pytest

from userauths.models import User
from coach.models import Coach
from client.models import Client
from services.userauths.enum import UserTypeChoices


@pytest.mark.django_db
def test_register_get(api_client):
    response = api_client.get('/auth/register/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_coach(api_client):
    response = api_client.post('/auth/register/', {
        'email': 'coach@mail.com',
        'password': 'Test@pass123',
        'full_name': 'Test Coach',
        'user_type': UserTypeChoices.coach
    })
    assert response.status_code == 201
    assert User.objects.filter(email='coach@mail.com').exists()
    assert Coach.objects.filter(user__email='coach@mail.com').exists()


@pytest.mark.django_db
def test_register_client(api_client):
    response = api_client.post('/auth/register/', {
        'email': 'client@mail.com',
        'password': 'Test@pass123',
        'full_name': 'Test Client',
        'user_type': UserTypeChoices.client
    })
    assert response.status_code == 201
    assert User.objects.filter(email='client@mail.com').exists()
    assert Client.objects.filter(user__email='client@mail.com').exists()


@pytest.mark.django_db
def test_register_email_exists(api_client, user):
    response = api_client.post('/auth/register/', {
        'email': 'user@mail.com', 
        'password': 'Test@pass183810jdf_'
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_missing_fields(api_client):
    response = api_client.post('/auth/register/', {
        'email': 'user@mail.com'
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_get(api_client):
    response = api_client.get('/auth/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(api_client, user):
    response = api_client.post('/auth/login/', {
        'email': user.email,
        'password': user.raw_password
    })
    assert response.status_code == 200
    assert User.objects.filter(email=user.email).exists()


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    response = api_client.post('/auth/login/', {
        'email': 'user@mail.com',
        'password': 'wrongPassword'
    })
    assert response.status_code == 401


@pytest.mark.django_db
def test_logout_get(api_client):
    response = api_client.get('/auth/logout/')
    assert response.status_code == 405


@pytest.mark.django_db
def test_logout(api_client, user):
    api_client.force_login(user)
    response = api_client.post('/auth/logout/')
    assert response.status_code == 200
