from django.db import models
from django.contrib.auth import models as auth_models


class Wallet(models.Model):
    balance = models.IntegerField(default=1000000)
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}__{self.balance}"