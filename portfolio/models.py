from django.db import models
from django.contrib.auth import models as auth_models
from markets import models as stock_models


class Order(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_models.Stock, on_delete=models.CASCADE)
    order_type = models.CharField(
        choices=(("BUY", "BUY"), ("SELL", "SELL")), max_length=20, default="BUY"
    )
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.user}__{self.stock}__{self.order_type}"


class Holding(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    stock = models.ForeignKey(stock_models.Stock, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user}__{self.stock}__{self.created_at}"
