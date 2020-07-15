from SVMReg import pre_process_data
import pandas
from SentimentAnalysis import get_date_polarity_and_subjectivity, average_polarity_subjectivity
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR

stock_data = pre_process_data()
stock_data = stock_data.set_index(pandas.Index(range(1, len(stock_data) + 1)))

Y_train = stock_data.iloc[0:int(0.8 * len(stock_data.index)), 1]
detrended_Y_train = []

for i in range(1, len(Y_train)):
    detrended_Y_train.append(Y_train[i+1] - Y_train[i])

Y_test = stock_data.iloc[int(0.8 * len(stock_data.index)):, 1]
detrended_Y_test = []

for i in range(len(Y_train) + 1, len(Y_train) + len(Y_test)):
    detrended_Y_test.append(Y_test[i+1] - Y_test[i])

sentiment_data = average_polarity_subjectivity(get_date_polarity_and_subjectivity())
sentiment_data = sentiment_data.sort_values(by = ["Date"], ascending=True)

polarity_train = sentiment_data.iloc[0:int(0.8 * len(sentiment_data.index)), 1]
subjectivity_train = sentiment_data.iloc[0:int(0.8 * len(sentiment_data.index)), 2]
polarity_test = sentiment_data.iloc[int(0.8 * len(sentiment_data.index)):, 1]
subjectivity_test = sentiment_data.iloc[int(0.8 * len(sentiment_data.index)):, 2]

date_train = stock_data.iloc[0:int(0.8*len(stock_data.index)), 0]
date_train = np.arange(len(date_train))
date_test = stock_data.iloc[int(0.8*len(stock_data.index)):, 0]
date_test = np.arange(len(date_test))
date_test = [x+len(date_train) for x in date_test]

polarity_train = np.array(polarity_train)
subjectivity_train = np.array(subjectivity_train)

polarity_test = np.array(polarity_test)
subjectivity_test = np.array(subjectivity_test)

X_date_train = date_train
date_train = date_train[1:]
polarity_train = polarity_train[1:]
subjectivity_train = subjectivity_train[1:]

X_train = np.array([date_train, polarity_train, subjectivity_train])
X_train = X_train.transpose()

X_date_test = date_test
date_test = date_test[1:]
polarity_test = polarity_test[1:]
subjectivity_test = subjectivity_test[1:]

X_test = np.array([date_test, polarity_test, subjectivity_test])
X_test = X_test.transpose()

detrended_Y_train = np.array(detrended_Y_train)
detrended_Y_train = detrended_Y_train.transpose()

detrended_Y_test = np.array(detrended_Y_test)
detrended_Y_test = detrended_Y_test.transpose()

svr = SVR(kernel = "rbf", C=1e3, gamma=0.00002) # test between 0.0003 and 0.0004
svr.fit(X_train, detrended_Y_train)

detrended_Y_predicted = svr.predict(X_test)


initial_test_price = stock_data.iloc[int(0.8 * len(stock_data.index)), 1]
current_price = initial_test_price
Y_test_prices = [initial_test_price]

for i in detrended_Y_test:
    current_price += i
    Y_test_prices.append(current_price)

current_price = initial_test_price
Y_predicted_prices = [initial_test_price]

for i in detrended_Y_predicted:
    current_price += i
    Y_predicted_prices.append(current_price)


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


print(mean_absolute_percentage_error(Y_test_prices, Y_predicted_prices))
print(mean_absolute_percentage_error(Y_test_prices[1:], detrended_Y_predicted))

print(detrended_Y_predicted)

plt.title("Sentiment Analysis + SVR")
plt.ylabel("Adjusted Close Price of Apple Stock ($)")
plt.xlabel("Date")
plt.plot(X_date_train, Y_train, label = "Training Dataset")
plt.plot(X_date_test, Y_test_prices, color = "red", label = "Testing Dataset")
plt.plot(X_date_test, Y_predicted_prices, color='green', linestyle = "dashed", linewidth=2, label = "Predicted Prices")
plt.legend(loc='upper left')

plt.figure(2)
plt.title("Detrended Predictions")
plt.ylim((-5, 5))
plt.ylabel("Daily Change in Apple Stock Price ($)")
plt.xlabel("Date")
plt.plot(date_train, detrended_Y_train, label = "Training Dataset")
plt.plot(date_test, detrended_Y_test, color = "red", label = "Testing Dataset")
plt.plot(date_test, detrended_Y_predicted, color = "green", linestyle = "dashed", linewidth = 2, label = "Predicted Change in Price")
plt.legend(loc='upper left')
plt.show()