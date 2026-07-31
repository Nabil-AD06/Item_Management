from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer,ProfileUpdateSerializer,UpdatePassword , CreateNewAdmin
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
# class TestView(APIView):
#     def get(sefl, requests) :
#         return Response({
#             "authenticated": requests.user.is_authenticated,
#             "id": requests.user.id,
#             "username": requests.user.username,
#             "email": requests.user.email,
#             "full_name": requests.user.full_name,
#             "department": requests.user.department,
# })

class ProfileUpdateView(APIView):
    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = request.user
            first_name = data["first_name"]
            last_name = data["last_name"]
            email = data["email"]
            try:
                # Mise à jour dans Keycloak
                KeycloakService.update_user(
                    user.keycloak_id,
                    first_name,
                    last_name,
                    email,
                )
                # Synchronisation de la base locale
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                return Response(
                    {
                        "message": "Profile updated successfully",
                        "user": {
                            "first_name": user.first_name,
                            "last_name":user.last_name,
                            "email": user.email,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            except Exception:
                raise
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    def get(self, request):
        user = request.user
    
        return Response(
            {
                "first_name": user.first_name,
                "last_name":user.last_name,
                "email": user.email,
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):

    def post(self, request):
        serializer = UpdatePassword(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]

        valid = KeycloakService.verifyCurrentPassword(
            user.username,
            current_password,
        )

        if not valid:
            return Response(
                {"current_password": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        KeycloakService.change_password(
            user.keycloak_id,
            new_password,
        )

        return Response(
            {"message": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )

class CreateAdminView(APIView):
    def post(self , request):
        serializer = CreateNewAdmin(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data
        username =data["username"]
        first_name=data["first_name"]
        last_name=data["last_name"]
        email=data["email"]
        password=data["password"]
        try:
            keycloak_id=KeycloakService.create_user(
               username=username,
               first_name=first_name,
               last_name=last_name,
               email=email,password=password,
        )
            Admin.objects.create(
               keycloak_id=keycloak_id,
               username=username,
               first_name=first_name,
               last_name=last_name,
               email=email,
        )
            return Response(
                {
                    "message" : "Admin created successfully !"
                },
                status=status.HTTP_201_CREATED
        )
        except Exception as e:
            return Response({"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
        
        