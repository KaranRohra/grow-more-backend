from django.urls import path
from portfolio import views

urlpatterns = [
    path("holdings/", views.HoldingAPI.as_view(), name="holdings")
]