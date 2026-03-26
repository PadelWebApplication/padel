from django.urls import path

from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("book-session/<service_id>/<coach_id>/", views.book_session, name="book_session"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
    path("payment_status/<billing_id>/", views.payment_status_page, name="payment_status"),

    path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
]
