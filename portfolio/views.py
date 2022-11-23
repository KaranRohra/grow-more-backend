import yfinance
from rest_framework import views
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions

from portfolio import models
from markets import models as market_models
from portfolio import serializers


class HoldingAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        portfolio = models.Holding.objects.filter(
            user=request.user).order_by("stock")
        data = serializers.HoldingSerializer(portfolio, many=True).data
        return Response(self.get_portfolio(data))

    def post(self, request):
        orderType = request.POST["type"]
        quantity = int(request.POST["quantity"])
        stock = market_models.Stock.objects.get(
            nse_symbol=request.POST["nse_symbol"])
        script = yfinance.Ticker(stock.nse_symbol+".NS").info
        price = script["regularMarketPrice"]

        if orderType == "buy":
            models.Holding.objects.create(user=request.user,
                price=price, quantity=quantity, stock=stock)
            return Response({"message": "Your order is placed"})
        else:
            holding_data = models.Holding.objects.filter(
                stock=stock).order_by("created_at")
            message = self.sell_stock(holding_data, quantity)
            return Response({"message": message})

    def sell_stock(self, holding_data, quantity):
        message = ""
        total_quantity = sum(
            [holding.quantity for holding in holding_data])

        if quantity > total_quantity:
            message = "You do not have "+str(quantity)+" shares"
            return message

        for holdings in holding_data:
            current_quantity = holdings.quantity
            if quantity >= current_quantity:
                holdings.delete()
                quantity -= current_quantity
            else:
                holdings.quantity = current_quantity-quantity
                holdings.save()
                break

        message = "Your order is placed"
        return message

    def get_portfolio(self, data):
        symbol, holding, quantity, sum = data[0]["stock"]["nse_symbol"], 0, 0, 0
        context = []
        for holding in data:
            if holding["stock"]["nse_symbol"] == symbol:
                sum += holding["quantity"]*holding["price"]
                quantity += holding["quantity"]
            else:
                context.append(
                    {
                        "symbol": symbol,
                        "quantity": quantity,
                        "price": round(sum/quantity, 2)
                    }
                )
                sum, quantity = holding["quantity"] * \
                    holding["price"], holding["quantity"]
                symbol = holding["stock"]["nse_symbol"]

        context.append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "price": round(sum/quantity, 2)
            }
        )

        return context
