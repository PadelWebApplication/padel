import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from base.models import Service, Session, Billing
from services.base.enum import SessionStatusChoices, BillingStatusChoices


@pytest.fixture
def service_with_image(service):
    image = SimpleUploadedFile(
        name='test_image.jpg', content=b'some image content', content_type='image/jpeg'
    )
    service.image = image
    service.save()
    yield service
    service.image.delete()


@pytest.fixture
def billing(db, client, session):
    return Billing.objects.create(
        client=client, session=session, sub_total=10, tax=15, total=11.5
    )


@pytest.mark.django_db
def test_service_creation(service):
    assert Service.objects.filter(id=service.id).exists()
    assert service.created is not None
    assert service.updated is not None


@pytest.mark.django_db
def test_service_image(service_with_image):
    assert service_with_image.image is not None
    assert 'test_image.jpg' in service_with_image.image.name


@pytest.mark.django_db
def test_service_name_too_long(service):
    with pytest.raises(Exception):
        service.name = 'x' * 256
        service.save()


@pytest.mark.django_db
def test_service_cost_too_big(service):
    with pytest.raises(Exception):
        service.cost = 10000000000
        service.save()


@pytest.mark.django_db
def test_service_available_coaches(service, coach):
    service.available_coaches.add(coach)
    assert service.available_coaches.filter(id=coach.id).exists()


@pytest.mark.django_db
def test_service_created_by(service, user, mock_user_id):
    with mock_user_id(user.id):
        service = Service.objects.create(name='Test service', cost=10)

    assert service.created_by == user


@pytest.mark.django_db
def test_service_updated_by(service, user, mock_user_id):
    with mock_user_id(user.id):
        service.name = 'Updated service'
        service.save()

    service.refresh_from_db()
    assert service.updated_by == user


@pytest.mark.django_db
def test_service_str(service):
    expected = f'{service.name} - {service.cost}'
    assert str(service) == expected


@pytest.mark.django_db
def test_session_creation(session):
    assert Session.objects.filter(id=session.id).exists()
    assert session.session_id is not None
    assert session.status == SessionStatusChoices.scheduled
    assert session.created is not None
    assert session.updated is not None


@pytest.mark.django_db
def test_session_id_unique(session):
    session1 = Session.objects.create()
    assert session.session_id != session1.session_id


@pytest.mark.django_db
def test_session_date(session):
    session.date = timezone.now()
    session.save()

    session.refresh_from_db()
    assert session.date is not None


@pytest.mark.django_db
def test_session_status(session):
    session.status = SessionStatusChoices.completed
    session.save()

    session.refresh_from_db()
    assert session.status == SessionStatusChoices.completed


@pytest.mark.django_db
def test_session_created_by(session, user, mock_user_id):
    with mock_user_id(user.id):
        session = Session.objects.create()

    assert session.created_by == user


@pytest.mark.django_db
def test_session_updated_by(session, user, mock_user_id):
    with mock_user_id(user.id):
        session.status = SessionStatusChoices.completed
        session.save()

    session.refresh_from_db()
    assert session.updated_by == user


@pytest.mark.django_db
def test_session_str(session):
    expected = f'{session.client.full_name} with {session.coach.full_name}'
    assert str(session) == expected


@pytest.mark.django_db
def test_session_service_set_null_when_service_deleted(service, session):
    service.delete()
    session.refresh_from_db()
    assert session.service is None


@pytest.mark.django_db
def test_session_coach_set_null_when_coach_deleted(coach, session):
    coach.delete()
    session.refresh_from_db()
    assert session.coach is None


@pytest.mark.django_db
def test_session_client_set_null_when_client_deleted(client, session):
    client.delete()
    session.refresh_from_db()
    assert session.client is None


@pytest.mark.django_db
def test_billing_creation(billing):
    assert Billing.objects.filter(id=billing.id).exists()
    assert billing.status == BillingStatusChoices.unpaid
    assert billing.date is not None
    assert billing.created is not None
    assert billing.updated is not None


@pytest.mark.django_db
def test_billing_id_unique(billing):
    billing1 = Billing.objects.create(sub_total=10, tax=10, total=11)
    assert billing.billing_id != billing1.billing_id


@pytest.mark.django_db
def test_billing_sub_total_too_big(billing):
    with pytest.raises(Exception):
        billing.sub_total = 10000000000
        billing.save()


@pytest.mark.django_db
def test_billing_tax_too_big(billing):
    with pytest.raises(Exception):
        billing.tax = 10000000000
        billing.save()


@pytest.mark.django_db
def test_billing_total_too_big(billing):
    with pytest.raises(Exception):
        billing.total = 10000000000
        billing.save()


@pytest.mark.django_db
def test_billing_status(billing):
    billing.status = BillingStatusChoices.paid
    billing.save()

    billing.refresh_from_db()
    assert billing.status == BillingStatusChoices.paid


@pytest.mark.django_db
def test_billing_created_by(user, mock_user_id):
    with mock_user_id(user.id):
        billing = Billing.objects.create(sub_total=10, tax=15, total=11.5)
    assert billing.created_by == user


@pytest.mark.django_db
def test_billing_updated_by(billing, user, mock_user_id):
    with mock_user_id(user.id):
        billing.status = BillingStatusChoices.paid
        billing.save()

    assert billing.updated_by == user


@pytest.mark.django_db
def test_billing_str(billing):
    expected = f'Billing for {billing.client.full_name} - Total: {billing.total}'
    assert str(billing) == expected


@pytest.mark.django_db
def test_billing_deleted_when_session_deleted(session, billing):
    session.delete()
    assert not Billing.objects.filter(id=billing.id).exists()
