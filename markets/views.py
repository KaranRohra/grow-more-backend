import yfinance
from rest_framework import views
from rest_framework.response import Response
from rest_framework import generics
from markets import models
from markets import serializers
from markets import data_feeder
from django.db import models as db_models


class StockSummaryAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        script = yfinance.Ticker(kwargs["symbol"]).info
        return Response(script)


class GetHistoricalAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        script = yfinance.Ticker(kwargs["symbol"])
        df = script.history(
            period=request.query_params["range"],
            interval=request.query_params["interval"],
        ).dropna()
        df = df[["Open", "High", "Low", "Close"]].to_dict("split")
        return Response(
            {"timestamp": df["index"], "ohlc": df["data"], "columns": df["columns"]}
        )


class GetCashflowAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            serializers.CashflowSerializer(
                models.Cashflow.objects.filter(stock__nse_symbol=kwargs["symbol"]),
                many=True,
            ).data
        )


class GetShareHoldingPatternAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            serializers.ShareHoldingPatternSerializer(
                models.ShareHoldingPattern.objects.filter(
                    stock__nse_symbol=kwargs["symbol"]
                ),
                many=True,
            ).data
        )


class GetQuarterlyResultsAPI(views.APIView):
    def get(self, request, **kwargs):
        qr = models.QuarterlyResult.objects.filter(stock__nse_symbol=kwargs["symbol"])
        return Response(serializers.QuarterlyResultSerializer(qr, many=True).data)


class GetProfitAndLossAPI(views.APIView):
    def get(self, request, symbol):
        return Response(
            serializers.ProfitAndLossSerializer(
                models.ProfitAndLoss.objects.filter(stock__nse_symbol=symbol), many=True
            ).data
        )


class GetBalanceSheetAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            serializers.BalanceSheetSerializer(
                models.BalanceSheet.objects.filter(stock__nse_symbol=kwargs["symbol"]),
                many=True,
            ).data
        )


class InsertStockDataAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        data_feeder.insert_financial_data()
        return Response()


class SearchStockAPI(generics.ListAPIView):
    serializer_class = serializers.StockSerializer
    queryset = models.Stock.objects.all()

    def get_queryset(self):
        lst = self.request.query_params["query"].split()
        stocks = []
        for stock in lst:
            stocks.extend(
                models.Stock.objects.filter(
                    db_models.Q(company_name__icontains=stock)
                    | db_models.Q(nse_symbol__icontains=stock)
                )
            )
        return stocks
