import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import QuandlScraper
from sklearn.metrics import mean_squared_error, r2_score

data = QuandlScraper.scrape_for_ticker("AAPL")
data = data.sort_values(by = ["Date"], ascending = True)

print(data)

X_train = data.iloc[0:int(0.8*len(data.index)), 0]
X_test = data.iloc[int(0.8*len(data.index) + 1):, 0]

Y_train = data.iloc[0:int(0.8*len(data.index)), 10]
Y_test = data.iloc[int(0.8*len(data.index) + 1):, 10]

X_train = np.arange(len(X_train))
X_train = np.reshape(X_train, (-1, 1))

X_test = np.arange(len(X_test))
X_test = np.reshape(X_test, (-1, 1))
X_test = [x+len(X_train) for x in X_test]

linReg = linear_model.LinearRegression()
linReg.fit(X_train, Y_train)

Y_predicted = linReg.predict(X_test)
print(linReg.coef_)
print(mean_squared_error(Y_test, Y_predicted))
print(r2_score(Y_test, Y_predicted))


plt.figure(1)
plt.ylabel("Adj_Close")
plt.xlabel("Date")
plt.plot(X_train, Y_train)
plt.plot(X_test, Y_test, color = "red")
plt.plot(X_test, Y_predicted, color='green', linestyle = "dashed", linewidth=2)
plt.show()