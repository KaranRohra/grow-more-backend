from django.urls import path
from markets import views


urlpatterns = [
    path("history/<str:symbol>/", views.GetHistoricalAPI.as_view(), name="historical-data"),
    path("summary/<str:symbol>/", views.StockSummaryAPI.as_view(), name="stock-summary"),

    # Data Feeding APIs
    path("insert-data/", views.InsertStockDataAPI.as_view(), name="insert-data"),
]
