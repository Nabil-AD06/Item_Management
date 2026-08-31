from rest_framework import serializers
from .models import Request , RequestItem , Equipment

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField()
    password = serializers.CharField()

class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()

class UpdatePassword(serializers.Serializer):
    current_password=serializers.CharField()
    new_password=serializers.CharField()
    confirm_password=serializers.CharField()

    def validate(self,data):
        if data["confirm_password"] != data["new_password"]:
            raise serializers.ValidationError(
                {"confirm_password" : "Password do not match"}
            )
        return data
class CreateNewAdmin(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password=serializers.CharField()
    confirm_password=serializers.CharField()

    def validate(self,data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password" : "Passwords do not match"}
            )
        return data

class RequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestItem
        fields = "__all__"
        extra_kwargs = {
            "request": {"read_only": True}
        }


class RequestSerializer(serializers.ModelSerializer):

    items = RequestItemSerializer(
        many=True
    )

    class Meta:
        model = Request
        fields = [
            "id",
            "request_id",
            "issue_date",
            "return_date",
            "employee_id",
            "employee_name",
            "employee_email",
            "department",
            "reason",
            "remarks",
            "date_issued",
            "created_at",
            "updated_at",
            "created_by",
            "based_on_stock",
            "overdue_email_sent",
            "items",
        ]
        extra_kwargs = {
            "created_by": {"read_only": True}
        }

    def update_stock(self, category, quantity_change):
        """
        quantity_change:
        positif  -> remettre du stock
        negatif  -> retirer du stock
        """

        equipment = Equipment.objects.filter(
            category=category,
            status="Available"
        ).first()

        if equipment:
            equipment.quantity += quantity_change
            equipment.save()

    def create(self, validated_data):

        items = validated_data.pop("items")

        request = Request.objects.create(
            **validated_data
        )

        for item in items:

            request_item = RequestItem.objects.create(
                request=request,
                **item
            )

            # Seulement si Based on stock + Issued
            if (
                request.based_on_stock
                and request_item.status == "Issued"
            ):
                self.update_stock(
                    request_item.accessory_req,
                    -request_item.quantity
                )

        return request

    def update(self, instance, validated_data):

        items = validated_data.pop(
            "items",
            None
        )
    
        # ==========================================
        # ANCIEN ÉTAT
        # ==========================================
    
        old_based_on_stock = instance.based_on_stock
    
        old_items = list(
            instance.items.all()
        )
    
        # ==========================================
        # NOUVEL ÉTAT DE BASED ON STOCK
        # ==========================================
    
        new_based_on_stock = validated_data.get(
            "based_on_stock",
            instance.based_on_stock
        )
    
        # ==========================================
        # RESTAURER L'ANCIEN STOCK
        #
        # On remet d'abord ce qui avait été retiré
        # par l'ancienne version de la request.
        # ==========================================
    
        if old_based_on_stock:
    
            for old_item in old_items:
    
                if old_item.status == "Issued":
    
                    self.update_stock(
                        old_item.accessory_req,
                        old_item.quantity
                    )
    
        # ==========================================
        # MODIFIER LA REQUEST
        # ==========================================
    
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        instance.save()
    
        # ==========================================
        # MODIFIER LES ITEMS
        # ==========================================
    
        if items is not None:
    
            instance.items.all().delete()
    
            for item in items:
    
                RequestItem.objects.create(
                    request=instance,
                    **item
                )
    
        # ==========================================
        # RETIRER LE NOUVEAU STOCK
        # ==========================================
    
        if new_based_on_stock:
    
            new_items = instance.items.all()
    
            for new_item in new_items:
    
                if new_item.status == "Issued":
    
                    self.update_stock(
                        new_item.accessory_req,
                        -new_item.quantity
                    )
    
        return instance



class EquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = "__all__"

from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at"]