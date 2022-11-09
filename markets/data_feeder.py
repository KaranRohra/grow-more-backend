import pandas as pd
from markets import models


def insert_nifty50_stocks():
    df = pd.read_csv("static/Nifty50.csv")
    nifty50 = []
    columns = list(df.columns)
    n = len(columns)
    for row in df.values:
        stock = {}
        for i in range(n):
            stock[columns[i]] = row[i]
        stock["yahoo_symbol"] = stock["nse_symbol"] + ".NS"

        nifty50.append(models.Stock(**stock))
    models.Stock.objects.bulk_create(nifty50)


def insert_financial_csv_data(filename, model):
    df = pd.read_csv(filename)
    df.column.fillna(0, inplace=True)
    columns, result = list(df.columns), []
    n = len(columns)
    for row in df.values:
        dic = {}
        for i in range(n):
            dic[columns[i]] = row[i]

        dic["stock"] = models.Stock.objects.get(nse_symbol=dic["symbol"])
        del dic["symbol"]
        result.append(model(**dic))
    model.objects.bulk_create(result)


def insert_financial_data():
    insert_nifty50_stocks()
    insert_financial_csv_data(
        filename="static/ShareHoldingPatternNifty50.csv",
        model=models.ShareHoldingPattern,
    )
    insert_financial_csv_data(
        filename="static/CashflowNifty50.csv",
        model=models.Cashflow,
    )
    insert_financial_csv_data(
        filename="static/QuarterlyResultsNifty50.csv",
        model=models.QuarterlyResult,
    )
    insert_financial_csv_data(
        filename="static/ProfitAndLossNifty50.csv",
        model=models.ProfitAndLoss,
    )
    insert_financial_csv_data(
        filename="static/BalanceSheetNifty50.csv",
        model=models.BalanceSheet,
    )
