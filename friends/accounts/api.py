from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegistrationSerializer, PasswordUpdateSerializer, EmailUpdateSerializer
from drf_yasg.utils import swagger_auto_schema


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={
            201: UserRegistrationSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=PasswordUpdateSerializer,
        responses={
            204: 'No Content',
            400: 'Bad Request'
        }
    )
    def put(self, request):
        user = request.user
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)
            print("Password updated successfully")
            return Response({"detail": "Password updated successfully"},status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmailUpdateSerializer,
        responses={
            200: EmailUpdateSerializer,
            400: 'Bad Request'
        }
    )
    def put(self, request):
        user = request.user
        serializer = EmailUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)