import pytest

from userauths.models import User


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        email='super@mail.com', password='Test@pass234723_L'
    )


@pytest.mark.django_db
def test_user_without_email_raises_error():
    with pytest.raises(Exception):
        User.objects.create_user(email='', password='Test@pass234723_L')


@pytest.mark.django_db
def test_user_creation(user):
    assert User.objects.filter(id=user.id)
    assert user.event_tracking_id is not None
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.created is not None
    assert user.updated is not None


@pytest.mark.django_db
def test_user_email_lowercased():
    user = User.objects.create_user(
        email='TEST@MAIL.COM', password='Test@pass183810jdf_'
    )
    assert user.email == 'test@mail.com'


@pytest.mark.django_db
def test_user_email_unique(user):
    with pytest.raises(Exception):
        User.objects.create_user(email='user@mail.com', password='Test@s183810jdf_')


@pytest.mark.django_db
def test_user_event_tracking_id_unique(user):
    user1 = User.objects.create_user(
        email='TEST@MAIL.COM', password='Test@pass183810jdf_'
    )
    assert user.event_tracking_id != user1.event_tracking_id


@pytest.mark.django_db
def test_user_activate(user):
    user.is_active = False
    user.save()
    user.activate()
    assert user.is_active is True


@pytest.mark.django_db
def test_user_deactivate(user):
    user.deactivate()
    assert user.is_active is False


@pytest.mark.django_db
def test_superuser_creation(superuser):
    assert User.objects.filter(id=superuser.id).exists()
    assert superuser.event_tracking_id is not None
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.is_active is True
    assert superuser.updated is not None
    assert superuser.created is not None


@pytest.mark.django_db
def test_superuser_must_have_is_staff():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@mail.com', password='Test@pass183810jdf_', is_staff=False
        )


@pytest.mark.django_db
def test_superuser_must_have_is_superuser():
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email='super@mail.com', password='Test@pass183810jdf_', is_superuser=False
        )