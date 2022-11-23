from nsetools import Nse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions

from portfolio import models
from markets import models as market_models


class HoldingAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        holdings = models.Holding.objects.filter(
            user=request.user).order_by("stock")
        return Response(self.get_holdings(holdings))

    def post(self, request):
        orderType = request.POST["type"]
        quantity = int(request.POST["quantity"])
        stock = market_models.Stock.objects.get(
            nse_symbol=request.POST["nse_symbol"])
        nse = Nse()
        detail = nse.get_quote(stock.nse_symbol)
        price = detail["lastPrice"]
        message = ""
        if orderType == "BUY":
            models.Holding.objects.create(user=request.user,
                                          price=price, quantity=quantity, stock=stock)
            message = "Your order is placed"
        elif orderType == "SELL":
            holding_data = models.Holding.objects.filter(
                stock=stock).order_by("created_at")
            message = self.sell_stock(holding_data, quantity)
        else:
            message = "Invalid order type"

        sum, total_quantity = 0, 0
        holding_data = models.Holding.objects.filter(
            user=request.user, stock=stock)
        if len(holding_data) == 0:
            return Response({"message": message})
        for holding in holding_data:
            sum += holding.price*holding.quantity
            total_quantity += holding.quantity
        return Response({"holding": {"price": round(sum/total_quantity, 2), "quantity": total_quantity, "symbol": stock.nse_symbol}, "message": message})

    def sell_stock(self, holding_data, quantity):
        total_quantity = sum(
            [holding.quantity for holding in holding_data])

        if quantity > total_quantity:
            return "You do not have "+str(quantity)+" shares"

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

    def get_holdings(self, holdings):
        symbol, quantity, sum = holdings.first().stock.nse_symbol, 0, 0
        context = []
        for holding in holdings:
            if holding.stock.nse_symbol == symbol:
                sum += holding.quantity*holding.price
                quantity += holding.quantity
            else:
                context.append(
                    {
                        "symbol": symbol,
                        "quantity": quantity,
                        "price": round(sum/quantity, 2)
                    }
                )
                sum, quantity = holding.quantity * \
                    holding.price, holding.quantity
                symbol = holding.stock.nse_symbol

        context.append(
            {
                "symbol": symbol,
                "quantity": quantity,
                "price": round(sum/quantity, 2)
            }
        )

        return context
