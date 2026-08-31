from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer,ProfileUpdateSerializer,UpdatePassword,CreateNewAdmin,RequestSerializer,EquipmentSerializer,CategorySerializer
from rest_framework import status , viewsets
from django.contrib.auth import authenticate
from .models import Admin , Request , RequestItem ,Equipment,Category
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
        
class CreateRequestView(APIView):

    def post(self, request):

        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created_request = serializer.save(
            created_by=request.user.username
        )
        return Response(
            {
                "message": "Request created successfully!"
            },
            status=status.HTTP_201_CREATED
        )
class RequestListView(APIView):

    def get(self, request):
        requests = Request.objects.all().order_by("-created_at")
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

class RequestDetailView(APIView):

    def put(self, request, pk):
        try:
            request_obj = Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response(
                {"error": "Request not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # =========================================
        # 1. Sauvegarder les anciens items
        # =========================================
        old_items = list(request_obj.items.all())

        # Dictionnaire pour retrouver facilement
        # l'ancien item par accessory_req
        old_items_dict = {
            item.accessory_req: item
            for item in old_items
        }

        # =========================================
        # 2. Valider la nouvelle request
        # =========================================
        serializer = RequestSerializer(
            request_obj,
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # =========================================
        # 3. Sauvegarder la modification
        # =========================================
        updated_request = serializer.save()

        # =========================================
        # 4. Gestion du stock
        # =========================================
        if updated_request.based_on_stock:

            new_items = list(
                updated_request.items.all()
            )

            for new_item in new_items:

                # Ancien item correspondant
                old_item = old_items_dict.get(
                    new_item.accessory_req
                )

                # Anciennes valeurs
                old_quantity = old_item.quantity if old_item else 0
                old_status = old_item.status if old_item else None

                # Nouvelles valeurs
                new_quantity = new_item.quantity
                new_status = new_item.status

                # =========================================
                # Quantité réellement prise du stock AVANT
                # =========================================
                old_used = (
                    old_quantity
                    if old_status == "Issued"
                    else 0
                )

                # =========================================
                # Quantité réellement prise du stock APRÈS
                # =========================================
                new_used = (
                    new_quantity
                    if new_status == "Issued"
                    else 0
                )

                # =========================================
                # Différence
                # =========================================
                difference = new_used - old_used

                # Rien à modifier
                if difference == 0:
                    continue

                # =========================================
                # Trouver le stock disponible
                # =========================================
                equipment = Equipment.objects.filter(
                    category=new_item.accessory_req,
                    status="Available"
                ).first()

                if not equipment:
                    continue

                # =========================================
                # Appliquer la différence
                # =========================================

                # Exemple :
                # old_used = 5
                # new_used = 8
                # difference = +3
                # => retirer 3 du stock

                if difference > 0:
                    equipment.quantity -= difference

                # Exemple :
                # old_used = 8
                # new_used = 3
                # difference = -5
                # => remettre 5 dans le stock

                else:
                    equipment.quantity += abs(difference)

                equipment.save()

        # =========================================
        # 5. Retourner la request
        # =========================================
        return Response(
            RequestSerializer(updated_request).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        try:
            request_obj = Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response(
                {"detail": "Request not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    
        # Restaurer le stock si la request était basée sur le stock
        # et que l'équipement était Issued
        if request_obj.based_on_stock:
    
            for item in request_obj.items.all():
    
                if item.status == "Issued":
    
                    equipment = Equipment.objects.filter(
                        category=item.accessory_req,
                        status="Available"
                    ).first()
    
                    if equipment:
                        equipment.quantity += item.quantity
                        equipment.save()
    
        # Supprimer la request
        request_obj.delete()
    
        return Response(
            {"detail": "Request deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class RequestItemDeleteView(APIView):

    def delete(self, request, pk):

        try:
            item = RequestItem.objects.get(pk=pk)
        except RequestItem.DoesNotExist:
            return Response(
                {"detail": "Item not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Récupérer la request liée à l'item
        request_obj = item.request

        # Si l'item était Issued et basé sur le stock,
        # on remet sa quantité dans le stock
        if request_obj.based_on_stock and item.status == "Issued":

            equipment = Equipment.objects.filter(
                category=item.accessory_req,
                status="Available"
            ).first()

            if equipment:
                equipment.quantity += item.quantity
                equipment.save()

        # Supprimer l'item
        item.delete()

        return Response(
            {"detail": "Item deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class EquipmentListCreateView(APIView):

    def get(self, request):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(
            equipments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = EquipmentSerializer(data=request.data)
    
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
        category = serializer.validated_data["category"]
        brand_model = serializer.validated_data["brand_model"]
        quantity = serializer.validated_data["quantity"]
    
        equipment = Equipment.objects.filter(
            category=category,
            brand_model=brand_model
        ).first()
    
        if equipment:
            equipment.quantity += quantity
    
            # Si un nouveau serial est fourni, on peut le mettre à jour
            serial_number = serializer.validated_data.get("serial_number", "")
            if serial_number:
                equipment.serial_number = serial_number
    
            equipment.save()
    
            return Response(
                EquipmentSerializer(equipment).data,
                status=status.HTTP_200_OK
            )
    
        equipment = serializer.save()
    
        return Response(
            EquipmentSerializer(equipment).data,
            status=status.HTTP_201_CREATED
        )

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer

class EquipmentDetailView(APIView):

    def get_object(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return None

    def put(self, request, pk):
        equipment = self.get_object(pk)
    
        if equipment is None:
            return Response(
                {"detail": "Equipment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    
        serializer = EquipmentSerializer(
            equipment,
            data=request.data
        )
    
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
        category = serializer.validated_data["category"]
        brand_model = serializer.validated_data["brand_model"]
        serial_number = serializer.validated_data.get("serial_number", "")
        new_quantity = serializer.validated_data["quantity"]
    
        # Chercher un autre équipement identique
        existing_equipment = Equipment.objects.filter(
            category=category,
            brand_model=brand_model,
            serial_number=serial_number
        ).exclude(
            id=equipment.id
        ).first()
    
        if existing_equipment:
            # Fusionner les quantités
            existing_equipment.quantity += new_quantity
            existing_equipment.save()
    
            # Supprimer l'ancien équipement
            equipment.delete()
    
            return Response(
                EquipmentSerializer(existing_equipment).data,
                status=status.HTTP_200_OK
            )

            # Aucun doublon → modification normale
        serializer.save()
    
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        equipment = self.get_object(pk)

        if equipment is None:
            return Response(
                {"detail": "Equipment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        equipment.delete()

        return Response(
            {"detail": "Equipment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )