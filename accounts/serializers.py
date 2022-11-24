from django.contrib.auth import models as auth_models
from accounts import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = auth_models.User(**validated_data)
        user.set_password(validated_data["password"])
        user.username = user.email
        user.save()
        return user

    class Meta:
        model = auth_models.User
        fields = ("id", "first_name", "last_name", "email", "password")


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wallet
        fields = "__all__"