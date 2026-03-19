from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from userauths import forms as userauths_forms
from coach import models as coach_models
from client import models as client_models


def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in.")
        return redirect("/")
    
    form = userauths_forms.UserRegisterForm(request.POST or None)
    


    if form.is_valid():
        user = form.save()
        full_name = form.cleaned_data.get("full_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user_type = form.cleaned_data.get("user_type")

        # user_ = authenticate(email=email, password=password)
        # login(request, user_)

        if user_type == "Coach":
            coach_models.Coach.objects.create(user=user, full_name=full_name)
        else:
            client_models.Client.objects.create(user=user, full_name=full_name, email=email)

        messages.success(request, "Account created successfully.")
        return redirect("/")

    context = {
        "form": form
    }

    return render(request, "userauths/sign-up.html", context)
