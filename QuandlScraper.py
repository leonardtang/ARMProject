import quandl
import pandas
import matplotlib.pyplot as plt


def plot_close_price_over_time(data):

    data.plot(y = "Adj_Close")
    plt.show()


def scrape_for_ticker(ticker):

    quandl.ApiConfig.api_key = "HndXjgaZLnHVKvR2WEyu"

    data = quandl.get(("EOD/" + ticker), start_date='2019-1-01', end_date='2019-3-01')

    return data


def write_to_excel(ticker):

    quandl.ApiConfig.api_key = "HndXjgaZLnHVKvR2WEyu"

    data = quandl.get(("EOD/" + ticker), start_date='2019-1-01', end_date='2019-3-01')
    data.reset_index()

    with pandas.ExcelWriter("quandlStocks.xlsx", engine = "xlsxwriter") as writer:
        data.to_excel(writer)

    writer.close()
    plot_close_price_over_time(data)


if __name__ == "__main__":
    write_to_excel(input("Scrape for which stock ticker?"))



