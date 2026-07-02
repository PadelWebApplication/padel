from django.urls import path

from base import views

app_name = "base"

urlpatterns = [
    path("", views.index, name="index"),
    path("service/<service_id>/", views.service_detail, name="service_detail"),
    path("service/<service_id>/buy_ticket/", views.buy_ticket, name="buy_ticket"),
    path("service/<service_id>/reserve_cash/", views.reserve_cash_ticket, name="reserve_cash_ticket"),
    path("book_session/<service_id>/<coach_id>/", views.book_session, name="book_session"),
    path("checkout/<billing_id>/", views.checkout, name="checkout"),
    path("payment_status/<billing_id>/", views.payment_status_page, name="payment_status"),

    path("stripe_payment/<billing_id>/", views.stripe_payment, name="stripe_payment"),
    path("stripe_payment_verify/<billing_id>/", views.stripe_payment_verify, name="stripe_payment_verify"),
]
