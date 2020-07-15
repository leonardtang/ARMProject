import numpy as np
import QuandlScraper
import matplotlib.pyplot as plt
import datetime
from sklearn.svm import SVR
import pandas


def pre_process_data():

    data = QuandlScraper.scrape_for_ticker("AAPL")
    data = data.sort_values(by = ["Date"], ascending = True)
    data = data.reset_index()
    data = data.drop(columns = ["Open", "High", "Low", "Close", "Volume", "Dividend",
                                "Split", "Adj_Open", "Adj_High", "Adj_Low", "Adj_Volume"])

    i = 0
    while i < len(data) - 1:

        date = data.iloc[i, 0].to_pydatetime().date()

        if date.isoweekday() == 5:

            if date == datetime.date(2019, 1, 18) or date == datetime.date(2019, 2, 15):
                saturday_price = (data.iloc[i, 1] + data.iloc[i + 1, 1]) / 2
                sunday_price = (saturday_price + data.iloc[i + 1, 1]) / 2
                monday_price = (sunday_price + data.iloc[i + 1, 1]) / 2
                weekend_prices = [saturday_price, sunday_price, monday_price]
                weekend_dates = [data.iloc[i, 0] + datetime.timedelta(days=1), data.iloc[i, 0] + datetime.timedelta(days=2),
                                 data.iloc[i, 0] + datetime.timedelta(days=3)]
                weekend = pandas.DataFrame({"Date": weekend_dates, "Adj_Close": weekend_prices})
                weekend = weekend.set_index([pandas.Index([i + 1, i + 2, i + 3])])
                data = pandas.concat([data.iloc[:i + 1], weekend, data.iloc[i + 1:]])
                i += 4

            else:

                saturday_price = (data.iloc[i, 1] + data.iloc[i + 1, 1]) / 2
                sunday_price = (saturday_price + data.iloc[i + 1, 1]) / 2
                weekend_prices = [saturday_price, sunday_price]
                weekend_dates = [data.iloc[i, 0] + datetime.timedelta(days=1), data.iloc[i, 0] + datetime.timedelta(days=2)]
                weekend = pandas.DataFrame({"Date": weekend_dates, "Adj_Close": weekend_prices})
                weekend = weekend.set_index([pandas.Index([i + 1, i + 2])])
                data = pandas.concat([data.iloc[:i + 1], weekend, data.iloc[i + 1:]])
                i += 3

        elif date.isoweekday != 6 and date.isoweekday != 7:
            i += 1

    return data


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def regression():

    data = pre_process_data()
    X_train = data.iloc[0:int(0.8*len(data.index)), 0]
    X_train = np.arange(len(X_train))
    X_train = np.reshape(X_train, (-1, 1))

    X_test = data.iloc[int(0.8*len(data.index) + 1):, 0]
    X_test = np.arange(len(X_test))
    X_test = [x+len(X_train) for x in X_test]
    X_test = np.reshape(X_test, (-1, 1))

    Y_train = data.iloc[0:int(0.8*len(data.index)), 1]
    Y_test = data.iloc[int(0.8*len(data.index) + 1):, 1]

    svr = SVR(kernel = "rbf", C=1e3, gamma=0.00015) # test between 0.0003 and 0.0004
    svr.fit(X_train, Y_train)

    Y_predicted = svr.predict(X_test)

    MAPE = mean_absolute_percentage_error(Y_test, Y_predicted)
    print(MAPE)

    plt.figure(1)
    plt.title("SVR RBF Baseline")
    plt.ylabel("Adjusted Close Price of Apple Stock ($)")
    plt.xlabel("Date")
    plt.plot(X_train, Y_train, label = "Training Dataset")
    plt.plot(X_test, Y_test, color = "red", label = "Testing Dataset")
    plt.plot(X_test, Y_predicted, color='green', linestyle = "dashed", linewidth=2, label = "Predicted Prices")
    plt.legend(loc = "upper left")
    plt.show()


if __name__ == "__main__":
    regression()
