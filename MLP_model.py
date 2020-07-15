import get_prices as hist
import tensorflow as tf
from preprocessing import DataProcessing
import quandl
import numpy as np
import pandas

# import pandas_datareader.data as pdr if using the single test below
# import fix_yahoo_finance as fix
# fix.pdr_override()

start = "2016-2-17"
end = "2019-2-17"

# hist.get_stock_data("AAPL", start_date=start, end_date=end)
#
# process = DataProcessing("quandlStocks.xlsx", 0.9)
# process.gen_test(10)
# process.gen_train(10)
#
# X_train = process.X_train
# tf.keras.utils.normalize(X_train)
# Y_train = process.Y_train
# tf.keras.utils.normalize(Y_train)
#
# X_test = process.X_test
# tf.keras.utils.normalize(X_test)
# Y_test = process.Y_test
# tf.keras.utils.normalize(Y_test)
#
# model = tf.keras.models.Sequential()
# model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
# model.add(tf.keras.layers.Dense(100, activation=tf.nn.relu))
# model.add(tf.keras.layers.Dense(1, activation=tf.nn.relu))
#
# model.compile(optimizer="adam", loss="mean_absolute_percentage_error")
#
# model.fit(X_train, Y_train, epochs=150)
#
# print(model.evaluate(X_test, Y_test))


quandl.ApiConfig.api_key = "HndXjgaZLnHVKvR2WEyu"

data = quandl.get_table('WIKI/PRICES', ticker=["AAPL"],
                            qopts={'columns': ['adj_close']},
                            date={'gte': '2019-1-17', 'lte': '2019-2-17'},
                            paginate=True)

with pandas.ExcelWriter("testStocks.xlsx", engine="xlsxwriter") as writer:
    data.to_excel(writer)
writer.close()

print(data)

# X_predict = np.reshape(data[1])
# X_predict = np.array("testStocks.xlsx"[0:]).reshape(10) / 200
# print(model.predict(X_predict)*200) ## denormalize this

# If instead of a full backtest, you just want to see how accurate the model is for a particular prediction, run this:
# data = pdr.get_data_yahoo("AAPL", "2017-12-19", "2018-01-03")
# stock = data["Adj Close"]
# X_predict = np.array(stock).reshape(10) / 200
# print(model.predict(X_predict)*200)

