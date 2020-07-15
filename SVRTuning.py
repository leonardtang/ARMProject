from sklearn.model_selection import GridSearchCV
import sklearn.svm as svm
import QuandlScraper
import numpy as np

parameters = {'kernel':'rbf', 'C':[1,2,3,4,5,6,7,8,9,10], 'gamma':
              [0.01,0.02,0.03,0.04,0.05,0.10,0.2,0.3,0.4,0.5]}
parameters = np.array(parameters)

data = QuandlScraper.scrape_for_ticker("AAPL")
data = data.sort_values(by = ["Date"], ascending = True)

X_train = data.iloc[0:int(0.8*len(data.index)), 0]
X_test = data.iloc[int(0.8*len(data.index) + 1):, 0]

Y_train = data.iloc[0:int(0.8*len(data.index)), 10]
Y_test = data.iloc[int(0.8*len(data.index) + 1):, 10]

X_train = np.arange(len(X_train))
X_train = np.reshape(X_train, (-1, 1))

X_test = np.arange(len(X_test))
X_test = np.reshape(X_test, (-1, 1))
X_test = [x+len(X_train) for x in X_test]

svr = svm.SVC()
grid = GridSearchCV(svr, parameters)
grid.fit(X_train, Y_train)
predicted = grid.predict(X_test)
cnf_matrix = confusion_matrix(Y_test, predicted)
print(cnf_matrix)
