import datetime as dt
import numpy as np


from nsepython import *
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from yahoo_fin import stock_info as si

scaler = MinMaxScaler(feature_range=(0, 1))


def convert_date(date):
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    dd, mm, yy = date.split('-')
    return [int(dd), months.get(mm), int(yy)]


def get_working_dates(n_days):
    n = 0
    today = dt.date.today()
    working_dates, holidays = [], []
    d = [data["tradingDate"] for data in nse_holidays()["SLBS"]]
    for data in d:
        dd, mm, yy = convert_date(data)
        holidays.append(dt.date(yy,mm,dd))
    while n < n_days:
        today += dt.timedelta(days=1)
        if today.weekday() not in [5, 6] and today not in holidays:
            working_dates.append(today)
            n += 1
    return working_dates



def forecast_price(symbol, forecast_days):
    last_n_days = forecast_days * 3  # Predict next day price based on 'last_n_days'
    price_df = si.get_data(symbol)
    price_df.dropna(inplace=True)
    close_price = price_df.filter(["close"])
    dataset = close_price.values

    predicted_price = predict_n_days(
        dataset[-last_n_days:], forecast_days, model=train_model(dataset, last_n_days)
    )

    return get_working_dates(forecast_days), predicted_price


def train_model(dataset, last_n_days):
    train_data = scaler.fit_transform(dataset)  # Scale the data

    x_train, y_train = [], []  # Split the data into x_train and y_train data sets

    for i in range(last_n_days, len(train_data)):
        x_train.append(train_data[i - last_n_days : i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(
        x_train, (x_train.shape[0], x_train.shape[1], 1)
    )  # Reshape x_train

    # Build the LSTM Model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer="adam", loss="mean_squared_error")  # Compile the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)  # Train the model

    return model


def predict_next_day(test_data, model):
    test_data = scaler.fit_transform(test_data)
    prediction = model.predict(np.array([test_data]))
    return scaler.inverse_transform(prediction)


def predict_n_days(
    n_days_dataset, forecast_days, model
):  # Prediction for next `forecast_days`
    forecasted_price, n_days_dataset = [], list(n_days_dataset)

    for _ in range(forecast_days):
        predicted_price = predict_next_day(test_data=n_days_dataset, model=model)[0]
        forecasted_price.append(predicted_price)

        n_days_dataset.append(predicted_price)
        n_days_dataset = n_days_dataset[1:]

    return forecasted_price
