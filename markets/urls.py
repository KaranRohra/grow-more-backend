from markets import views
from django.urls import path

urlpatterns = [
    path("historical-data/<str:symbol>/<str:interval>/<str:range>",
         views.GetHistoricalAPI.as_view(), name="historical-data")
]
