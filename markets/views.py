from rest_framework.response import Response
import yfinance
from rest_framework import views
from markets import models
from markets import serializers


class GetHistoricalAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        symbol = kwargs["symbol"]
        interval = request.query_params["interval"]
        range = request.query_params["range"]
        script = yfinance.Ticker(symbol)
        df = script.history(period=range, interval=interval)
        df = df[["Open", "High", "Low", "Close"]].to_dict("split")
        return Response(
            {
            "timestamp": df["index"], 
            "ohlc": df["data"],
            "columns": df["columns"]
            }
        )

class GetProfitAndLossAPI(views.APIView):
    def get(self, request, symbol):
        return Response(serializers.ProfitAndLossSerializers(
            models.ProfitAndLoss.objects.filter(stock__nse_symbol = symbol),
            many=True
        ).data);