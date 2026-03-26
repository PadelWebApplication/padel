from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse

import stripe

from base import models as base_models
from coach import models as coach_models
from client import models as client_models

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
        billing.status = "Unpaid"
        billing.save()

        return redirect("base:checkout", billing.billing_id)
        

    context = {
        "service": service,
        "coach": coach,
        "client": client
    }

    return render(request, "base/book_session.html", context)


@login_required
def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    context = {
        "billing": billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    }

    return render(request, "base/checkout.html", context)


@csrf_exempt
def stripe_payment(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=billing.client.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "USD",
                    "product_data": {
                        "name": billing.client.full_name
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
        if billing.status == "Unpaid":
            billing.status = "Paid"
            billing.save()
            billing.session.status = "Completed"
            billing.session.save()

            coach_models.Notification.objects.create(
                coach=billing.session.coach,
                session=billing.session,
                type="New Session"
            )

            client_models.Notification.objects.create(
                client=billing.session.client,
                session=billing.session,
                type="Session Scheduled"
            )

            return redirect(f"/payment_status/{billing.billing_id}/?payment_status=paid")
    else:
        return redirect(f"/payment_status/{billing.billing_id}/?payment_status=failed")
    

@login_required
def payment_status_page(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")

    context = {
        "billing": billing,
        "payment_status": payment_status
    }

    return render(request, "base/payment_status.html", context)
