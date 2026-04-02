from django.urls import path

from client import views

app_name = "client"

urlpatterns = [
    path("", view=views.dashboard, name="dashboard"),
    path("sessions/", view=views.sessions, name="sessions"),
    path("session_detail/<session_id>/", view=views.session_detail, name="session_detail"),

    path("cancel_session/<session_id>/", view=views.cancel_session, name="cancel_session"),
    
]
