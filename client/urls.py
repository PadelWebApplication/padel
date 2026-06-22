from django.urls import path

from client import views

app_name = "client"

urlpatterns = [
    path("", view=views.dashboard, name="dashboard"),
    path("sessions/", view=views.sessions, name="sessions"),
    path("session_detail/<session_id>/", view=views.session_detail, name="session_detail"),

    path("cancel_session/<session_id>/", view=views.cancel_session, name="cancel_session"),

    path("payments/", view=views.payments, name="payments"),
    path("notifications/", view=views.notifications, name="notifications"),
    path("mark_notifications_seen/<notification_id>/", view=views.mark_notifications_seen, name="mark_notifications_seen"),
    path("profile/", view=views.profile, name="profile"),
    
]
