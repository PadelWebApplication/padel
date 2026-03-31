from django.urls import path

from coach import views

app_name = "coach"

urlpatterns = [
     path("", views.dashboard, name="dashboard"),
     path("sessions/", views.sessions, name="sessions"),
     path("session_detail/<session_id>/", views.session_detail, name="session_detail"),
]
