from django.urls import path

from coach import views

app_name = "coach"

urlpatterns = [
     path("", views.dashboard, name="dashboard")
]
