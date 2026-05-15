from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout

from userauths.serializers import RegisterSerializer, LoginSerializer
from coach import models as coach_models
from client import models as client_models
from userauths.models import User


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            full_name = serializer.validated_data.get('full_name')
            user_type = serializer.validated_data.get('user_type')

            user = User.objects.create_user(email=email, password=password)

            user_authenticate = authenticate(request, email=email, password=password)
            login(request, user_authenticate)

            if user_type == 'Coach':
                coach_models.Coach.objects.create(user=user, full_name=full_name)
            else:
                client_models.Client.objects.create(
                    user=user, full_name=full_name, email=email
                )

            return Response(
                {'message': 'Account created successfully'},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return Response(
                    {'message': 'Login successful'}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
