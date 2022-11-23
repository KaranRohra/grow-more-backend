from django.urls import path
from portfolio import views

urlpatterns = [
    path("holding/",views.HoldingAPI.as_view(),name="portfolio")
]