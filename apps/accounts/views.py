from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.permissions import UnrestrictedPermission
from .serializers import UserSerializer, LoginSerializer
from django.utils import timezone
from django.db import connection


class SignupView(APIView):
    permission_classes = [UnrestrictedPermission]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "phone": user.phone,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [UnrestrictedPermission]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Manually update the last_login field
                user.last_login = timezone.now()
                user.save()

                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response(
                    {
                        "message": "Login successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": "Invalid email or password. Please check your credentials."
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    """
    Simple API endpoint to check if the application is healthy.
    """

    def get(self, request):
        try:
            connection.ensure_connection()
            return Response({"status": "success", "message": "Service is healthy"})
        except Exception as e:
            print(e)
            return Response({"status": "fail", "message": "Database error"}, status=500)
