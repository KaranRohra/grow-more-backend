from markets import views
from django.urls import path

urlpatterns = [
    path("historical/<str:symbol>/",views.GetHistoricalAPI.as_view(), name="historical-data"),
    path("<str:symbol>/profit-and-loss",views.GetProfitAndLossAPI.as_view(), name="profit-and-loss"),
]
