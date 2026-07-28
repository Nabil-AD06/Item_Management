from rest_framework import serializers

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
