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
