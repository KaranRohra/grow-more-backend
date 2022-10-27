from rest_framework import serializers
from markets import models


class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BalanceSheet
        fields = "__all__"
