from django.urls import path

from coach import views

app_name = "coach"

urlpatterns = [
     path("", views.dashboard, name="dashboard"),
     path("sessions/", views.sessions, name="sessions"),
     path("session_detail/<session_id>/", views.session_detail, name="session_detail"),
     
     path("cancel_session/<session_id>/", views.cancel_session, name="cancel_session"),
     path("activate_session/<session_id>/", views.activate_session, name="activate_session"),
     path("complete_session/<session_id>/", views.complete_session, name="complete_session"),
]
