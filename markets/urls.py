from markets import views
from django.urls import path

urlpatterns = [
    path("historical/<str:symbol>/",
         views.GetHistoricalAPI.as_view(), name="historical-data")
]
