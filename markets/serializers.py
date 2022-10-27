from dataclasses import fields
from markets import models
from rest_framework import serializers


class QuarterlyResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuarterlyResult
        fields = "__all__"