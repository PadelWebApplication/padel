from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from userauths.serializers import RegisterSerializer, LoginSerializer
from coach import models as coach_models
from client import models as client_models
from userauths.models import User


def get_next_url(request):
    next_url = request.data.get('next') or request.query_params.get('next')

    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url

    return None


def redirect_after_auth(request):
    next_url = get_next_url(request)
    if next_url:
        return redirect(next_url)

    try:
        request.user.coach
        return redirect("coach:dashboard")
    except coach_models.Coach.DoesNotExist:
        pass

    try:
        request.user.client
        return redirect("client:dashboard")
    except client_models.Client.DoesNotExist:
        pass

    return redirect("base:index")


class RegisterView(APIView):
    def get(self, request):
        return render(
            request,
            'userauths/register.html',
            {'next_url': request.GET.get('next', '')},
        )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            full_name = serializer.validated_data.get('full_name')

            user = User.objects.create_user(email=email, password=password)

            user_authenticate = authenticate(request, email=email, password=password)
            login(request, user_authenticate)

            client_models.Client.objects.create(
                user=user, full_name=full_name, email=email
            )

            return redirect_after_auth(request)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def get(self, request):
        return render(
            request,
            'userauths/login.html',
            {'next_url': request.GET.get('next', '')},
        )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect_after_auth(request)
            else:
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return redirect("base:index")


class ForgotPasswordView(APIView):
    def get(self, request):
        return render(request, 'userauths/forgot_password.html')

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'userauths/forgot_password.html', status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User with this email was not found")
            return render(request, 'userauths/forgot_password.html', status=404)

        user.set_password(password)
        user.save()
        messages.success(request, "Password updated successfully. Please log in.")
        return redirect("userauths:login")
