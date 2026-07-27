from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer,ProfileUpdateSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Admin
from services.keycloak_service import KeycloakService

class LoginView(APIView) :
    def post(self , request) :
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid() :
            data = serializer.validated_data
            login = data["email_or_username"]
            try :
                user_obj = Admin.objects.get(email=login)
                username =user_obj.username
            except Admin.DoesNotExist:
                username = login
            user = authenticate(
                username = username,
                password=data["password"]
            )
            if user is None:
                return Response(
                    {
                        "error" : "invalid username or password"
                    },
                    status = status.HTTP_401_UNAUTHORIZED
                )
            return Response(
                {
                    "message" : "Login with succes",
                    "user" : {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                }
                },
                status = status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class TestView(APIView):
    def get(sefl, requests) :
        return Response({
            "authenticated": requests.user.is_authenticated,
            "id": requests.user.id,
            "username": requests.user.username,
            "email": requests.user.email,
            "full_name": requests.user.full_name,
            "department": requests.user.department,
})

class ProfileUpdateView(APIView):
    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            username = data["username"]
            email = data["email"]
            try:
                # Mise à jour dans Keycloak
                KeycloakService.update_user(
                    user.keycloak_id,
                    username,
                    email,
                )
                # Synchronisation de la base locale
                user.username = username
                user.email = email
                user.save()
                return Response(
                    {
                        "message": "Profile updated successfully",
                        "user": {
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception as e:
                return Response(
                    {
                        "error": str(e)
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    def get(self, request):
        user = request.user
    
        return Response(
            {
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )
    