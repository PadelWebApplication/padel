from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

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


def checkout(request, billing_id):
    billing = base_models.Billing.objects.get(billing_id=billing_id)

    context = {
        "billing": billing,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "paypal_client_id": settings.PAYPAL_CLIENT_ID
    }

    return render(request, "base/checkout.html", context)
