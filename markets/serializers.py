from rest_framework import serializers
from markets import models


class ProfitAndLoss(serializers.ModelSerializer):
    class Meta:
        model = models.ProfitAndLoss
        fields = "__all__"
