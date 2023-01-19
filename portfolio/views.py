from yahoo_fin import stock_info as si
from rest_framework import views
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status

from portfolio import models
from portfolio import serializers
from markets import models as market_models
from accounts import models as auth_models


class ProfitLossAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        holdings = models.Order.objects.filter(user=request.user, order_type="SELL")
        total_pl, total_pl_percent = 0, 0
        for holding in holdings:
            total_pl += holding.profit_loss
            total_pl_percent += holding.percentage_pl

        return Response({
            "Total Returns": round(total_pl,2),
            "Total Returns Percentage": round(total_pl_percent,2),
        })

class OrderHistoryAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        order_history = models.Order.objects.filter(user=request.user).order_by(
            "-created_at", "stock"
        )
        return Response(
                serializers.OrderHistory(order_history, many=True).data
        )

class HoldingAPI(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def get(self, request):
        holdings = models.Holding.objects.filter(user=request.user).order_by(
            "stock", "-created_at"
        )
        return Response(get_holdings(holdings))

    def post(self, request):
        quantity = int(request.data["quantity"])
        stock = market_models.Stock.objects.get(nse_symbol=request.data["nse_symbol"])
        price = round(si.get_live_price(stock.yahoo_symbol),2)
        wallet = auth_models.Wallet.objects.get(user=request.user)

        if request.data["type"] == "BUY":
            response = self.buy_stock(wallet, price, request.user, quantity, stock)
        elif request.data["type"] == "SELL":
            if quantity == 0:
                response = {
                    "message": "Quantity cannot be zero"
                }
            else: 
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

        holdings = models.Holding.objects.filter(user=user).order_by(
            "stock", "-created_at"
        )
        
        holdings = get_holdings(holdings)
        total_holdings = [holding for holding in holdings if holding["Symbol"] == stock.nse_symbol]
        total_pl = round(quantity*price - quantity * total_holdings[0]["Avg Price"], 2)
        total_pl_percentage = round((total_pl * 100) / (quantity * total_holdings[0]["Avg Price"]), 2)
        print(total_pl_percentage)

        wallet.balance += price * quantity
        wallet.save()
        models.Order.objects.create(
            user=user, stock=stock, order_type="SELL", quantity=quantity, price=price, profit_loss=total_pl, percentage_pl=total_pl_percentage
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

def get_holdings(holdings):
    context, index, n = [], 0, len(holdings)
    while index < n:
        sm, quantity = 0, 0
        symbol = holdings[index].stock.nse_symbol
        ltp = si.get_live_price(holdings[index].stock.yahoo_symbol)
        

        while index < n and holdings[index].stock.nse_symbol == symbol:
            sm += holdings[index].quantity * holdings[index].price
            quantity += holdings[index].quantity
            index += 1
        
        avg_price = round(sm / quantity, 2)
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
    
    return context
