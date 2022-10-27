from django.urls import path
from markets import views


urlpatterns = [
    path("historical/<str:symbol>/", views.GetHistoricalAPI.as_view(), name="historical-data"),
    path("<str:symbol>/quarterly-result/", views.GetQuarterlyResultsAPI.as_view(), name="quarterly-result")
]
