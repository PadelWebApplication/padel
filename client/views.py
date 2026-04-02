from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models

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

