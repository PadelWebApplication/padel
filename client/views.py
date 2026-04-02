from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from marshmallow import ValidationError

from client import models as client_models
from base import models as base_models

@login_required
def dashboard(request):
    client = client_models.Client.objects.get(user=request.user)
    sessions = base_models.Session.objects.filter(client=client)
    notifications = client_models.Notification.objects.filter(client=client, seen=False)
    total_spent = base_models.Billing.objects.filter(client=client).aggregate(total_spent=models.Sum("total"))["total_spent"]

    context = {
        "sessions": sessions,
        "notifications": notifications,
        "total_spent": total_spent,
    }

    return render(request, "client/dashboard.html", context)


@login_required
def sessions(request):
    client = client_models.Client.objects.get(user=request.user)
    sessions = base_models.Session.objects.filter(client=client)

    context = {
        "sessions": sessions,
    }

    return render(request, "client/sessions.html", context)


@login_required
def session_detail(request, session_id):
    client = client_models.Client.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, client=client)

    session_note = base_models.SessionNote.objects.filter(session=session).first()
    action_items = base_models.ActionItem.objects.filter(session=session)
    resources = base_models.Resource.objects.filter(session=session)

    context = {
        "session": session,
        "session_note": session_note,
        "action_items": action_items,
        "resources": resources,
    }

    return render(request, "client/session_detail.html", context)


@login_required
def cancel_session(request, session_id):
    client = client_models.Client.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, client=client)

    session.status = "Cancelled"
    session.save()

    messages.success(request, "Session Cancelled Successfully")
    return redirect("client:session_detail", session.session_id)


@login_required
def payments(request):
    client = client_models.Client.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(session__client=client, status="Paid")

    context = {
        "payments": payments,
    }

    return render(request, "client/payments.html", context)

@login_required
def notifications(request):
    client = client_models.Client.objects.get(user=request.user)
    notifications = client_models.Notification.objects.filter(client=client, seen=False)

    context = {
        "notifications": notifications,
    }

    return render(request, "client/notifications.html", context)


@login_required
def mark_notifications_seen(request, notification_id):
    client = client_models.Client.objects.get(user=request.user)
    notifications = client_models.Notification.objects.get(client=client, id=notification_id)
    notifications.seen = True
    notifications.save()

    messages.success(request, "Notification marked as seen")
    return redirect("client:notifications")

@login_required
def profile(request):
    client = client_models.Client.objects.get(user=request.user)
    
    if request.method == "POST":
        image = request.FILES.get("image")

        if image:
            client.image = image

        full_name = request.POST.get("full_name")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        email = request.POST.get("email")
        gender = request.POST.get("gender")

        dob = request.POST.get("dob")
        
        if dob:
            try:
                client.dob = dob
            except ValidationError:
                messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
        
        client.image = image
        client.full_name = full_name
        client.mobile = mobile
        client.address = address
        client.email = email
        client.gender = gender
        client.dob = dob

        if image != None:
            client.image = image

        client.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect("client:profile")

    context = {
        "client": client,
    }

    return render(request, "client/profile.html", context)
