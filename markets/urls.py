from django.urls import path
from markets import views


urlpatterns = [
<<<<<<< HEAD
    path("stock-info/<str:symbol>/", views.StockInfo.as_view(), name="stock-info"),
    path("historical-data/<str:symbol>/<str:interval>/<str:range>", views.GetHistoricalAPI.as_view(), name="historical-data")
=======
    path("historical/<str:symbol>/", views.GetHistoricalAPI.as_view(), name="historical-data")
>>>>>>> 26d36fa0e45764c5a1ffe69a562118b10e685930
]
