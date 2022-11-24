from nsetools import Nse
from rest_framework import views
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status

from portfolio import models
from markets import models as market_models
from accounts import models as auth_models


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
        quantity = int(request.data["quantity"])
        stock = market_models.Stock.objects.get(nse_symbol=request.data["nse_symbol"])
        price = nse.get_quote(stock.nse_symbol)["lastPrice"]
        wallet = auth_models.Wallet.objects.get(user=request.user)

        if request.data["type"] == "BUY":
            response = self.buy_stock(wallet, price, request.user, quantity, stock)
        elif request.data["type"] == "SELL":
            response = self.sell_stock(
                models.Holding.objects.filter(user=request.user, stock=stock).order_by(
                    "created_at"
                ),
                quantity,
                wallet,
                price,
                request.user,
                stock,
            )
        else:
            response = {
                "message": "Invalid order type",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        sm, total_quantity = 0, 0
        holding_data = models.Holding.objects.filter(user=request.user, stock=stock)
        if len(holding_data) == 0:
            return Response(response)
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
                **response,
                "wallet_balance": wallet.balance,
            }
        )

    def buy_stock(self, wallet, price, user, quantity, stock):
        if wallet.balance >= price * quantity:
            models.Holding.objects.create(
                user=user, price=price, quantity=quantity, stock=stock
            )
            models.Order.objects.create(
                user=user,
                stock=stock,
                order_type="BUY",
                quantity=quantity,
                price=price,
            )
            wallet.balance -= price * quantity
            wallet.save()
            return {"message": "Buy order is placed", "status": status.HTTP_200_OK}
        return {
            "message": "Insufficient Balance",
            "status": status.HTTP_400_BAD_REQUEST,
        }

    def sell_stock(self, holding_data, quantity, wallet, price, user, stock):
        total_quantity = sum([holding.quantity for holding in holding_data])

        if quantity > total_quantity:
            return {
                "message": f"You don't have {quantity} quantity of {stock.nse_symbol} shares",
                "status": status.HTTP_400_BAD_REQUEST,
            }

        wallet.balance += price * quantity
        wallet.save()
        models.Order.objects.create(
            user=user, stock=stock, order_type="SELL", quantity=quantity, price=price
        )

        for holdings in holding_data:
            current_quantity = holdings.quantity
            if quantity >= current_quantity:
                holdings.delete()
                quantity -= current_quantity
            else:
                holdings.quantity = current_quantity - quantity
                holdings.save()
                break

        return {
            "message": "Your order placed successfully",
            "status": status.HTTP_200_OK,
        }

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
