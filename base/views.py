import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import stripe

from base import models as base_models
from coach import models as coach_models
from client import models as client_models
from services.base.enum import BillingStatusChoices, SessionStatusChoices
from services.coach.enum import NotificationTypeChoices as CoachNotificationTypeChoices
from services.client.enum import NotificationTypeChoices as ClientNotificationTypeChoices

def index(request):
    services = base_models.Service.objects.all()
    context = {
        "services": services
    }

    return render(request, "base/index.html", context)


def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)
    context = {
        "service": service
    }

    return render(request, "base/service_detail.html", context)


def buy_ticket(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    if service.is_sold_out:
        messages.error(request, "This event is sold out.")
        return redirect("base:service_detail", service.id)

    client = None
    if request.user.is_authenticated:
        client, _ = client_models.Client.objects.get_or_create(
            user=request.user,
            defaults={
                "full_name": request.user.email,
                "email": request.user.email,
            },
        )

    coach = service.available_coaches.first()

    session = base_models.Session.objects.create(
        service=service,
        coach=coach,
        client=client,
        session_date=coach.next_available_session_date if coach else None,
    )

    billing = base_models.Billing.objects.create(
        client=client,
        session=session,
        guest_email=client.email if client else None,
        sub_total=service.cost,
        tax=service.cost * 5 / 100,
        total=service.cost + (service.cost * 5 / 100),
        status=BillingStatusChoices.unpaid,
    )

    return redirect("base:checkout", billing.billing_id)


@login_required
def reserve_cash_ticket(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    if service.is_sold_out:
        messages.error(request, "This event is sold out.")
        return redirect("base:service_detail", service.id)

    client, _ = client_models.Client.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.email,
            "email": request.user.email,
        },
    )
    coach = service.available_coaches.first()

    session = base_models.Session.objects.create(
        service=service,
        coach=coach,
        client=client,
        session_date=coach.next_available_session_date if coach else None,
        status=SessionStatusChoices.pending,
    )

    billing = base_models.Billing.objects.create(
        client=client,
        session=session,
        guest_email=client.email,
        sub_total=service.cost,
        tax=service.cost * 5 / 100,
        total=service.cost + (service.cost * 5 / 100),
        status=BillingStatusChoices.reserved,
    )

    client_models.Notification.objects.create(
        client=client,
        session=session,
        type=ClientNotificationTypeChoices.session_scheduled,
    )
    if coach:
        coach_models.Notification.objects.create(
            coach=coach,
            session=session,
            type=CoachNotificationTypeChoices.new_session,
        )

    messages.success(request, "Ticket reserved. You can pay with cash at the venue.")
    return redirect(f"/payment_status/{billing.billing_id}/?payment_status=reserved")


@login_required
def book_session(request, service_id, coach_id):
    service = base_models.Service.objects.get(id=service_id)
    coach = coach_models.Coach.objects.get(id=coach_id)
    client = client_models.Client.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        dob = request.POST.get("dob")

        client.full_name = full_name
        client.email = email
        client.mobile = mobile
        client.gender = gender
        client.address = address
        client.dob = dob
        client.save()

        session = base_models.Session.objects.create(
            service=service,
            coach=coach,
            client=client,
            session_date=coach.next_available_session_date
        )

        billing = base_models.Billing()
        billing.client = client
        billing.session = session
        billing.sub_total = session.service.cost
        billing.tax = session.service.cost * 5 / 100
        billing.total = billing.sub_total + billing.tax
        billing.status = BillingStatusChoices.unpaid
        billing.save()

        return redirect("base:checkout", billing.billing_id)
        

    context = {
        "service": service,
        "coach": coach,
        "client": client
    }

    return render(request, "base/book_session.html", context)


def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    context = {
        "billing": billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "payment_currency": settings.PAYMENT_CURRENCY,
    }

    return render(request, "base/checkout.html", context)


def set_billing_email_from_request(request, billing):
    try:
        data = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        data = {}

    email = (data.get("email") or request.GET.get("email") or "").strip()
    if email:
        billing.guest_email = email
        if billing.client and not billing.client.email:
            billing.client.email = email
            billing.client.save()
        billing.save()

    return billing.recipient_email


def send_invoice_email(billing):
    recipient_email = billing.recipient_email
    if not recipient_email:
        return

    merge_data = {
        "billing": billing,
        "payment_currency": settings.PAYMENT_CURRENCY,
    }
    subject = f"Invoice for {billing.session.service.name}"
    text_body = render_to_string("email/invoice.txt", merge_data)
    html_body = render_to_string("email/invoice.html", merge_data)

    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.FROM_EMAIL,
        to=[recipient_email],
        body=text_body,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


@csrf_exempt
def stripe_payment(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    recipient_email = set_billing_email_from_request(request, billing)
    if not recipient_email:
        return JsonResponse({"message": "Email is required"}, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=recipient_email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": settings.PAYMENT_CURRENCY.lower(),
                    "product_data": {
                        "name": billing.session.service.name
                    },
                    "unit_amount": int(billing.total * 100)
                },
                "quantity": 1
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", 
                                                       args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", 
                                                       args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"
    )
    return JsonResponse({"sessionId": checkout_session.id})


def stripe_payment_verify(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == "paid":
        if billing.status == BillingStatusChoices.unpaid:
            billing.status = BillingStatusChoices.paid
            billing.save()
            billing.session.status = SessionStatusChoices.scheduled
            billing.session.save()

            if billing.session.coach:
                coach_models.Notification.objects.create(
                    coach=billing.session.coach,
                    session=billing.session,
                    type=CoachNotificationTypeChoices.new_session
                )

            if billing.session.client:
                client_models.Notification.objects.create(
                    client=billing.session.client,
                    session=billing.session,
                    type=ClientNotificationTypeChoices.session_scheduled
                )

            try:
                merge_data = {
                    "billing": billing,
                }

                if billing.session.coach:
                    subject = "New Session"
                    text_body = render_to_string("email/new_session.txt", merge_data)
                    html_body = render_to_string("email/new_session.html", merge_data)

                    msg = EmailMultiAlternatives(
                        subject=subject,
                        from_email=settings.FROM_EMAIL,
                        to=[billing.session.coach.user.email],
                        body=text_body
                    )
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()

                send_invoice_email(billing)
            except Exception as e:
                print(f"Email failed to send: {e}")

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    

def payment_status_page(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing": billing,
        "payment_status": payment_status
    }

    return render(request, "base/payment_status.html", context)
