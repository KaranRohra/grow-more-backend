from django.urls import path
from markets import views


urlpatterns = [
    path("history/<str:symbol>/", views.GetHistoricalAPI.as_view(), name="historical-data"),
    path("summary/<str:symbol>/", views.StockSummaryAPI.as_view(), name="stock-summary"),
    path("<str:symbol>/cashflow/", views.GetCashflowAPI.as_view(), name="cashflow"),
    path("<str:symbol>/share-holding-pattern/", views.GetShareHoldingPatternAPI.as_view(), name="share-holding-pattern"),
    path("<str:symbol>/quarterly-result/", views.GetQuarterlyResultsAPI.as_view(), name="quarterly-result"),
    path("<str:symbol>/profit-and-loss/",views.GetProfitAndLossAPI.as_view(), name="profit-and-loss"),
    path("<str:symbol>/balance-sheet/", views.GetBalanceSheetAPI.as_view(), name="balance-sheet"),

    # Data Feeding APIs
    path("insert-data/", views.InsertStockDataAPI.as_view(), name="insert-data"),
]
