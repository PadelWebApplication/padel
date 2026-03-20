from django.urls import path

from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-session/<service_id>/<coach_id>/", views.book_session, name="book_session"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
]
