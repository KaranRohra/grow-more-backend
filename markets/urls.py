from django.urls import path
from markets import views


urlpatterns = [
    path("stock-info/<str:symbol>/", views.StockInfo.as_view(), name="stock-info"),
    path("historical-data/<str:symbol>/<str:interval>/<str:range>", views.GetHistoricalAPI.as_view(), name="historical-data")
]
