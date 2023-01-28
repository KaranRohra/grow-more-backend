import yfinance
from yahoo_fin import stock_info as si
from rest_framework import views
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import authentication
from rest_framework import permissions

from django.db import models as db_models
from markets import models
from markets import serializers
from markets import data_feeder
from markets import forecast


class PricePredictionAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(forecast.forecast_price(request.query_params["symbol"], int(request.query_params["forecast_days"])))


class StockSummaryAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        summary = si.get_quote_data(kwargs["symbol"])
        summary["longBusinessSummary"] = "It is summary"
        stock = models.Stock.objects.filter(yahoo_symbol=kwargs["symbol"]).first()
        summary.update(serializers.StockSerializer(stock).data)
        return Response(summary)

class GetHistoricalAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        df = get_symbol_history(
            kwargs["symbol"],
            request.query_params["range"],
            request.query_params["interval"],
        )
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


class GetStockPeerAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        stock = models.Stock.objects.get(nse_symbol=kwargs["symbol"])
        peers = (
            models.Stock.objects.filter(industry=stock.industry)
            .exclude(nse_symbol=kwargs["symbol"])
            .values_list("nse_symbol", flat=True)
        )
        symbols = [kwargs["symbol"]]
        symbols.extend(peers)
        return Response(design_chart(symbols[0:3]))


class GetComparisonAPI(views.APIView):
    def get(self, request):
        return Response(design_chart(request.query_params["symbols"].split()))


def get_symbol_history(symbol, period, interval):
    script = yfinance.Ticker(symbol)
    df = script.history(
        period=period,
        interval=interval,
    ).dropna()
    return df[["Open", "High", "Low", "Close"]].to_dict("split")


def design_chart(symbols):
    data = []
    result = {
        "percent_change": [],
    }
    for symbol in symbols:
        df = get_symbol_history(symbol + ".NS", "1y", "1wk")
        data.append({"timestamp": df["index"], "close": df["data"]})

    for i in range(0, len(data)):
        closing_prices = data[i]["close"]
        y = []
        for j in range(0, len(closing_prices)):
            y.append(
                round(
                    (
                        (closing_prices[j][0] - closing_prices[0][0])
                        / closing_prices[0][0]
                    )
                    * 100,
                    2,
                )
            )
        result["percent_change"].append({"symbol": symbols[i], "y": y})
    result["x"] = data[0]["timestamp"]
    return result
