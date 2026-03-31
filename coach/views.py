from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from coach import models as coach_models
from base import models as base_models

@login_required
def dashboard(request):
    coach = coach_models.Coach.objects.get(user=request.user)
    sessions = base_models.Session.objects.filter(coach=coach)
    notifications = coach_models.Notification.objects.filter(coach=coach)

    context = {
        "sessions": sessions,
        "notifications": notifications,
    }

    return render(request, "coach/dashboard.html", context)


@login_required
def sessions(request):
    coach = coach_models.Coach.objects.get(user=request.user)
    sessions = base_models.Session.objects.filter(coach=coach)

    context = {
        "sessions": sessions,
    }

    return render(request, "coach/sessions.html", context)


@login_required
def session_detail(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    session_notes = base_models.SessionNote.objects.filter(session=session)
    action_items = base_models.ActionItem.objects.filter(session=session)
    resources = base_models.Resource.objects.filter(session=session)

    context = {
        "session": session,
        "session_notes": session_notes,
        "action_items": action_items,
        "resources": resources,
    }

    return render(request, "coach/session_detail.html", context)
    
