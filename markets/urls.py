from django.urls import path
from markets import views


urlpatterns = [
    path("summary/", views.SummaryAPI.as_view(), name="summary"),
    path("stock-info/<str:symbol>/", views.StockInfo.as_view(), name="stock-info"),
]