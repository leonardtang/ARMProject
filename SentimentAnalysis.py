import pandas
import datetime
from textblob import TextBlob


data = pandas.read_excel(r"C:\Users\harry\PycharmProjects\ARMProject\AppleTweets\AppleTweets.xlsx")
dates = data["DATE"]
tweets = data["TWEET"]


def get_date_polarity_and_subjectivity():

    days_since = []
    polarity = []
    subjectivity = []

    for tweet in tweets:
        tweet = TextBlob(tweet)
        p = tweet.polarity
        polarity.append(p)
        s = tweet.subjectivity
        subjectivity.append(s)

    first_day = datetime.datetime(2019, 1, 1)

    for date in dates:
        day = (date - first_day).days + 1
        days_since.append(day)

    d = {"Date": days_since, "Polarity": polarity, "Subjectivity": subjectivity}
    df = pandas.DataFrame(d)
    return df


def write_to_excel(d):

    with pandas.ExcelWriter("AveragedSentimentData.xlsx", engine = "xlsxwriter") as writer:
        d.to_excel(writer)


def average_polarity_subjectivity(df):

    average_polarity = []
    average_subjectivity = []
    date = []

    sum_polarity = df.iloc[0, 1]
    sum_subjectivity = df.iloc[0, 2]

    count = 1
    i = 0
    current_day = df.iloc[0, 0]

    while i < len(df):

        while df.iloc[i, 0] == current_day:
            count += 1
            sum_polarity += df.iloc[i, 1]
            sum_subjectivity += df.iloc[i, 2]
            if i != len(df) - 1:
                i += 1
            elif i == len(df) - 1:
                break

        a_p = sum_polarity / count
        average_polarity.append(a_p)
        a_s = sum_subjectivity / count
        average_subjectivity.append(a_s)

        sum_polarity = df.iloc[i, 1]
        sum_subjectivity = df.iloc[i, 2]

        date.append(df.iloc[i - 1, 0])
        current_day = df.iloc[i, 0]
        count = 1

        if i != len(df) - 1:
            i += 1
        elif i == len(df) - 1:
            break

    d = {"Date": date, "Average Polarity": average_polarity, "Average Subjectivity": average_subjectivity}
    df = pandas.DataFrame(d)
    return df

write_to_excel(average_polarity_subjectivity(get_date_polarity_and_subjectivity()))
