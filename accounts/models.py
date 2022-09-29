from django.db import models
from django.contrib.auth import models as auth_models

class User(auth_models.AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = "email"
    username = None
    REQUIRED_FIELDS = []

