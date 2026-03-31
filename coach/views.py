from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
    

@login_required
def cancel_session(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    session.status = "Cancelled"
    session.save()

    messages.success(request, "Session Cancelled Successfully")
    return redirect("coach:session_detail", session.session_id)


@login_required
def activate_session(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    session.status = "Scheduled"
    session.save()

    messages.success(request, "Session Re-Scheduled Successfully")
    return redirect("coach:session_detail", session.session_id)

@login_required
def complete_session(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    session.status = "Completed"
    session.save()

    messages.success(request, "Session Completed Successfully")
    return redirect("coach:session_detail", session.session_id)


@login_required
def add_session_note(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    if request.method == "POST":
        summary = request.POST.get("summary")
        client_mindset = request.POST.get("client_mindset")
        coach_observations = request.POST.get("coach_observations")
        
        base_models.SessionNote.objects.create(session=session, summary=summary, 
                                               client_mindset=client_mindset, coach_observations=coach_observations)

        messages.success(request, "Session Note Added Successfully")
        return redirect("coach:session_detail", session.session_id)
    

@login_required
def edit_session_note(request, session_id, session_note_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)
    session_note = base_models.SessionNote.objects.get(id=session_note_id, session=session)

    if request.method == "POST":
        summary = request.POST.get("summary")
        client_mindset = request.POST.get("client_mindset")
        coach_observations = request.POST.get("coach_observations")

        session_note.summary = summary
        session_note.client_mindset = client_mindset
        session_note.coach_observations = coach_observations
        session_note.save()

        messages.success(request, "Session Note Updated Successfully")
        return redirect("coach:session_detail", session.session_id)

