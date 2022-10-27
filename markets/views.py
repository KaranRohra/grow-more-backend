import yfinance
from rest_framework import views
from rest_framework.response import Response
from markets import models
from markets import serializers


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


class GetBalanceSheetAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            serializers.BalanceSheetSerializer(
                models.BalanceSheet.objects.filter(stock__nse_symbol=kwargs["symbol"]),
                many=True,
            ).data
        )
