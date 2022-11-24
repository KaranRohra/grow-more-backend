from nsetools import Nse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions

from portfolio import models
from markets import models as market_models
from accounts import models as auth_models
from accounts import serializers 

nse = Nse()


class HoldingAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        holdings = models.Holding.objects.filter(user=request.user).order_by(
            "stock", "-created_at"
        )
        return Response(self.get_holdings(holdings))

    def post(self, request):
        quantity = int(request.POST["quantity"])
        stock = market_models.Stock.objects.get(nse_symbol=request.POST["nse_symbol"])
        price = nse.get_quote(stock.nse_symbol)["lastPrice"]
        message = None
        wallet = auth_models.Wallet.objects.get(user=request.user)

        if request.POST["type"] == "BUY":
            if wallet.balance >= price*quantity:
                models.Holding.objects.create(
                    user=request.user, price=price, quantity=quantity, stock=stock
                )
                wallet.balance -= price*quantity
                wallet.save()
                message = "Buy order is placed"
                models.Order.objects.create(user=request.user, stock=stock, order_type="BUY", quantity=quantity, price=price)
            else:
                message = "Insufficient Balance"
        elif request.POST["type"] == "SELL":
            message = self.sell_stock(
                models.Holding.objects.filter(user=request.user, stock=stock).order_by(
                    "created_at"
                ),
                quantity,
                wallet,
                price
            )   
            # if message:
            #     message = "Sell order placed"
            #     wallet.balance += price*quantity
            #     wallet.save()
            #     models.Order.objects.create(user=request.user, stock=stock, order_type="SELL", quantity=quantity, price=price)
            # else:
            #     message = "Insufficient shares"
        else:
            message = "Invalid order type"

        sm, total_quantity = 0, 0
        holding_data = models.Holding.objects.filter(user=request.user, stock=stock)
        if len(holding_data) == 0:
            return Response({"message": message})
        for holding in holding_data:
            sm += holding.price * holding.quantity
            total_quantity += holding.quantity
        return Response(
            {
                "holding": {
                    "price": round(sm / total_quantity, 2),
                    "quantity": total_quantity,
                    "symbol": stock.nse_symbol,
                },
                "message": message,
                "wallet_balance": wallet.balance,
            }
        )

    def sell_stock(self, holding_data, quantity, wallet, price):
        total_quantity = sum([holding.quantity for holding in holding_data])

        if quantity > total_quantity:
            return "You do not have " + str(quantity) + " shares"
            # return False

        for holdings in holding_data:
            current_quantity = holdings.quantity
            if quantity >= current_quantity:
                holdings.delete()
                quantity -= current_quantity
            else:
                holdings.quantity = current_quantity - quantity
                holdings.save()
                break
        
        wallet.balance += price*quantity
        wallet.save()
        return "Sell order is placed"
        # return True

    def get_holdings(self, holdings):
        symbol, quantity, sum = holdings[0].stock.nse_symbol, 0, 0
        context = []

        for i in range(len(holdings)):
            holding = holdings[i]
            if holding.stock.nse_symbol != symbol or i == len(holdings) - 1:
                ltp = nse.get_quote(symbol)["lastPrice"]
                avg_price = round(sum / quantity, 2)
                context.append(
                    {
                        "Symbol": symbol,
                        "Quantity": quantity,
                        "Avg Price": avg_price,
                        "LTP": round(ltp, 2),
                        "Current Value": round(ltp * quantity, 2),
                        "P&L": round((ltp - avg_price) * quantity, 2),
                        "Net Change": round((ltp - avg_price) * 100 / avg_price, 2),
                    }
                )
                symbol, sum, quantity = holding.stock.nse_symbol, 0, 0, 0

            sum += holding.quantity * holding.price
            quantity += holding.quantity

        return context
