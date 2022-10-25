from django.shortcuts import render
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import views
import yfinance
from rest_framework.response import Response


class StockInfo(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request, symbol):
        script = yfinance.Ticker(symbol).info
        return Response(script)

class SummaryAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        global_market = {
            "equity_market": ["^DJI", "^IXIC", "^GDAXI", "IN-V22.SI", "^RUT"],
            "commodity_market": ["CL=F", "NG=F", "GC=F", "SI=F"],
            "crypto_market": ["BTC-USD", "ETH-USD", "LTC-USD", "XRP-USD"],
            "currency_market": ["INR=X", "GBPINR=X", "EURINR=X", "JPYINR=X"],
        }
        result = {}
        for key in global_market:
            result[key] = []
            for symbols in global_market[key]:
                script = yfinance.Ticker(symbols).info
                result[key].append({
                    "symbol" : symbols,
                    "regularMarketPrice" : script["regularMarketPrice"],
                })
        return Response(result)


