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

    session_note = base_models.SessionNote.objects.get(session=session)
    action_items = base_models.ActionItem.objects.filter(session=session)
    resources = base_models.Resource.objects.filter(session=session)

    context = {
        "session": session,
        "session_note": session_note,
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

@login_required
def add_action_item(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    if request.method == "POST":
        task = request.POST.get("task")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        is_completed = request.POST.get("is_completed") == "on"

        base_models.ActionItem.objects.create(
            session=session, 
            task=task, 
            description=description, 
            due_date=due_date if due_date else None, 
            is_completed=is_completed
        )

        messages.success(request, "Action Item Added Successfully")
        return redirect("coach:session_detail", session.session_id)
    

@login_required
def edit_action_item(request, session_id, action_item_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)
    action_item = base_models.ActionItem.objects.get(id=action_item_id, session=session)

    if request.method == "POST":
        task = request.POST.get("task")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        is_completed_raw = request.POST.get("is_completed")
        is_completed = True if is_completed_raw == "on" else False

        action_item.task = task
        action_item.description = description
        action_item.due_date = due_date if due_date else None
        action_item.is_completed = is_completed
        action_item.save()

        messages.success(request, "Action Item Updated Successfully")
        return redirect("coach:session_detail", session.session_id)
    
@login_required
def add_resource(request, session_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)

    if request.method == "POST":
        title = request.POST.get("title")
        link = request.POST.get("link")
        file = request.FILES.get("file")
        
        base_models.Resource.objects.create(
            session=session, 
            title=title, 
            link=link, 
            file=file
        )

        messages.success(request, "Resource Added Successfully")
        return redirect("coach:session_detail", session.session_id)
    

@login_required
def edit_resource(request, session_id, resource_id):
    coach = coach_models.Coach.objects.get(user=request.user)
    session = base_models.Session.objects.get(session_id=session_id, coach=coach)
    resource = base_models.Resource.objects.get(id=resource_id, session=session)

    if request.method == "POST":
        title = request.POST.get("title")
        link = request.POST.get("link")
        file = request.FILES.get("file")
        if file:
            resource.file = file

        resource.title = title
        resource.link = link
        resource.file = file
        resource.save()

        messages.success(request, "Resource Updated Successfully")
        return redirect("coach:session_detail", session.session_id)
