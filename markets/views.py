from django.shortcuts import HttpResponse
import yfinance
from rest_framework import views
# Create your views here.
class GetHistoricalAPI(views.APIView):
    def get(self, request, **kwargs):
        symbol = kwargs["symbol"]
        interval = kwargs["interval"]
        range = kwargs["range"]

        script = yfinance.Ticker(symbol)

        df = script.history(period=range, interval=interval)
        df = df[["Open", "High", "Low", "Close", "Volume"]].to_dict("split")
        timestamp = df["index"]
        columns = df["columns"]
        data = df["data"]
        context={
            "timestamp" : timestamp[0],
            "data":data[0],
            "columns":columns
        }
        return HttpResponse(context)