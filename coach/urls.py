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

     path("add_session_note/<session_id>/", views.add_session_note, name="add_session_note"),
     path("edit_session_note/<session_id>/<session_note_id>/", views.edit_session_note, name="edit_session_note"),

     path("add_action_item/<session_id>/", views.add_action_item, name="add_action_item"),
     path("edit_action_item/<session_id>/<action_item_id>/", views.edit_action_item, name="edit_action_item"),

     path("add_resource/<session_id>/", views.add_resource, name="add_resource"),
     path("edit_resource/<session_id>/<resource_id>/", views.edit_resource, name="edit_resource"),

     path("payments/", views.payments, name="payments"),
     

]
