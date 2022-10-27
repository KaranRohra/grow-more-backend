from django.urls import path
from markets import views


urlpatterns = [
    path("historical/<str:symbol>/", views.GetHistoricalAPI.as_view(), name="historical-data"),
    path("quaterly-result/<str:symbol>/", views.GetQuarterlyResultsAPI.as_view(), name="quarterly-result")
]
