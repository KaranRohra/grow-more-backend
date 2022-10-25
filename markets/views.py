from rest_framework import authentication
from rest_framework import permissions
from rest_framework import views
import yfinance
from rest_framework.response import Response
from django.shortcuts import HttpResponse

class StockInfo(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, symbol):
        script = yfinance.Ticker(symbol).info
        return Response(script)


class GetHistoricalAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        symbol = kwargs["symbol"]
        interval = kwargs["interval"]
        range = kwargs["range"]
        script = yfinance.Ticker(symbol)
        df = script.history(period=range, interval=interval)
        df = df[["Open", "High", "Low", "Close", "Volume"]].to_dict("split")
        timestamp = df["index"]
        columns = df["columns"]
        data = df["data"]
        context = {
            "timestamp": timestamp[0],
            "data": data[0],
            "columns": columns
        }
        return HttpResponse(context)
