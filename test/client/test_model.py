import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from client.models import Client, Notification
from services.client.enum import NotificationTypeChoices


@pytest.fixture
def client_with_image(client):
    image = SimpleUploadedFile(
        name='test_image.jpg', content=b'some image content', content_type='image/jpeg'
    )
    client.image = image
    client.save()
    yield client
    client.image.delete()


@pytest.fixture
def notification(db, client, session):
    return Notification.objects.create(client=client, session=session)


@pytest.mark.django_db
def test_client_creation(client):
    assert Client.objects.filter(id=client.id).exists()
    assert client.updated is not None
    assert client.created is not None


@pytest.mark.django_db
def test_client_image(client_with_image):
    assert client_with_image is not None
    assert 'test_image.jpg' in client_with_image.image.name


@pytest.mark.django_db
def test_client_created_by(user, client_user, mock_user_id):
    with mock_user_id(user.id):
        client = Client.objects.create(user=client_user)

    assert client.created_by == user


@pytest.mark.django_db
def test_client_updated_by(user, client, mock_user_id):
    with mock_user_id(user.id):
        client.full_name = 'Test Name'
        client.save()

    client.refresh_from_db()
    assert client.updated_by == user


@pytest.mark.django_db
def test_client_str(client):
    expected = f'{client.full_name}'
    assert str(client) == expected


@pytest.mark.django_db
def test_client_deleted_when_user_deleted(client_user, client):
    client_user.delete()
    assert not Client.objects.filter(id=client.id).exists()


@pytest.mark.django_db
def test_notification_creation(notification):
    assert Notification.objects.filter(id=notification.id).exists()
    assert notification.type == NotificationTypeChoices.session_scheduled
    assert notification.seen is False
    assert notification.date is not None
    assert notification.created is not None
    assert notification.updated is not None


@pytest.mark.django_db
def test_notification_type(notification):
    notification.type = NotificationTypeChoices.session_cancelled
    notification.save()

    notification.refresh_from_db()
    assert notification.type == NotificationTypeChoices.session_cancelled


@pytest.mark.django_db
def test_notification_seen(notification):
    notification.seen = True
    notification.save()

    notification.refresh_from_db()
    assert notification.seen is True


@pytest.mark.django_db
def test_notification_str(notification):
    expected = f'{notification.client.full_name} Notification'
    assert str(notification) == expected


@pytest.mark.django_db
def test_notification_client_set_null(notification, client):
    client.delete()
    notification.refresh_from_db()
    assert notification.client is None


@pytest.mark.django_db
def test_notification_created_by(user, mock_user_id):
    with mock_user_id(user.id):
        notification = Notification.objects.create()

    assert notification.created_by == user


@pytest.mark.django_db
def test_notification_updated_by(user, notification, mock_user_id):
    with mock_user_id(user.id):
        notification.type = NotificationTypeChoices.session_cancelled
        notification.save()

    notification.refresh_from_db()
    assert notification.updated_by == user


@pytest.mark.django_db
def test_notification_deleted_when_session_deleted(notification, session):
    session.delete()
    assert not Notification.objects.filter(id=notification.id).exists()
