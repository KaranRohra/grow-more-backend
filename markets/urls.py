from django.urls import path
from markets import views


urlpatterns = [
    path("history/<str:symbol>/", views.GetHistoricalAPI.as_view(), name="historical-data"),
    path("summary/<str:symbol>/", views.StockSummaryAPI.as_view(), name="stock-summary"),
    path("<str:symbol>/cashflow/", views.GetCashflowAPI.as_view(), name="cashflow"),
    path("<str:symbol>/share-holding-pattern/", views.GetShareHoldingPatternAPI.as_view(), name="share-holding-pattern"),
    path("<str:symbol>/quarterly-results/", views.GetQuarterlyResultsAPI.as_view(), name="quarterly-result"),
    path("<str:symbol>/profit-and-loss/",views.GetProfitAndLossAPI.as_view(), name="profit-and-loss"),
    path("<str:symbol>/balance-sheet/", views.GetBalanceSheetAPI.as_view(), name="balance-sheet"),
    path("<str:symbol>/peers/", views.GetStockPeerAPI().as_view(), name="peers"),
    path("comparison/", views.GetComparisonAPI().as_view(), name="comparison"),
    path("search/", views.SearchStockAPI.as_view(), name="search-stock"),
    path("forecast/", views.PricePredictionAPI().as_view(), name="price-prediction"), 

    # Data Feeding APIs
    path("insert-data/", views.InsertStockDataAPI.as_view(), name="insert-data"),
]
