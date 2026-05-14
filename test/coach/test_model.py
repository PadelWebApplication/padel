import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from coach.models import Coach, Notification
from services.coach.enum import NotificationTypeChoices

@pytest.fixture
def coach_with_image(coach):
    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=b'some image content',
        content_type='image/jpeg'
    )
    coach.image = image
    coach.save()
    yield coach
    coach.image.delete()


@pytest.fixture
def notification(db, coach, session):
    return Notification.objects.create(coach=coach, session=session)


@pytest.mark.django_db
def test_coach_creation(coach):
    assert Coach.objects.filter(id=coach.id).exists()
    assert coach.updated is not None
    assert coach.created is not None


@pytest.mark.django_db
def test_coach_image(coach_with_image):
    assert coach_with_image.image is not None
    assert 'test_image.jpg' in coach_with_image.image.name


@pytest.mark.django_db
def test_coach_str(coach):
    expected = f'Coach {coach.full_name}'
    assert str(coach) == expected


@pytest.mark.django_db
def test_coach_created_by(user, coach_user, mock_user_id):
    with mock_user_id(user.id):
        coach = Coach.objects.create(user=coach_user)

    assert coach.created_by == user


@pytest.mark.django_db
def test_coach_updated_by(user, coach, mock_user_id):
    with mock_user_id(user.id):
        coach.full_name = 'Test Name'
        coach.save()

    coach.refresh_from_db()
    assert coach.updated_by == user


@pytest.mark.django_db
def test_coach_deleted_when_user_deleted(coach_user, coach):
    coach_user.delete()
    assert not Coach.objects.filter(id=coach.id).exists()


@pytest.mark.django_db
def test_notification_creation(notification):
    assert Notification.objects.filter(id=notification.id).exists()
    assert notification.type == NotificationTypeChoices.new_session
    assert notification.seen is False
    assert notification.date is not None
    assert notification.updated is not None
    assert notification.created is not None


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
    expected = f'Coach {notification.coach.full_name} Notification'
    assert str(notification) == expected


@pytest.mark.django_db
def test_notification_coach_set_null(notification, coach):
    coach.delete()
    notification.refresh_from_db()
    assert notification.coach is None


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
