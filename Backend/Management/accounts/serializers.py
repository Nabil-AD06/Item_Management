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
        source="requestitem_set",
        many=True)

    class Meta:
        model = Request
        fields = "__all__"
        extra_kwargs = {
            "created_by": {"read_only": True}
        }

    def create(self, validated_data):
        items = validated_data.pop("requestitem_set")

        request = Request.objects.create(**validated_data)

        for item in items:
            RequestItem.objects.create(
                request=request,
                **item
            )

        return request
    def update(self, instance, validated_data):
        items = validated_data.pop("requestitem_set", None)
    
        # Modifier les champs de la Request
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
    
        instance.save()
    
        # Modifier les équipements
        if items is not None:
            instance.requestitem_set.all().delete()
    
            for item in items:
                RequestItem.objects.create(
                    request=instance,
                    **item
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