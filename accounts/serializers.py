from accounts import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = models.User(**validated_data, is_staff=True, is_superuser=True)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = models.User
        fields = ("id", "first_name", "last_name", "email", "password", "phone_number")