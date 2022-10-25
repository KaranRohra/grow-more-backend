import yfinance
from rest_framework import views
from rest_framework.response import Response

class StockInfo(views.APIView):
    def get(self, request, symbol):
        script = yfinance.Ticker(symbol).info
        return Response(script)


class GetHistoricalAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        symbol = kwargs["symbol"]
        interval = request.query_params["interval"]
        range = request.query_params["range"]
        script = yfinance.Ticker(symbol)
        df = script.history(period=range, interval=interval)
        df = df[["Open", "High", "Low", "Close"]].to_dict("split")
        return Response(
            {"timestamp": df["index"], "ohlc": df["data"], "columns": df["columns"]}
        )
