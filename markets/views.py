import yfinance
import pandas as pd
from rest_framework import views
from rest_framework.response import Response
from markets import models
from markets import serializers
from markets import data_feeder


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
        )
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


class InsertStockDataAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        data_feeder.insert_financial_data()
        return Response()
