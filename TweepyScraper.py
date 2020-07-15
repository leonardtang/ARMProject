import tweepy
import pandas
from datetime import timedelta


def twitter_setup():

    auth = tweepy.OAuthHandler("PD5i0stSP2lJb5vLQrzl8VUAd", "0ImWBcm9llocr6KDcZfSOYUvQNvDSGFqL2318RZptZJ3dodcOE")
    auth.set_access_token("1465656516-1dRixj1zKf2EyEa8TSn3BnS5kt2ro7n8uauxg2N", "BTaP41chvQFyOm8gnjALKXK2BHa9qISBVKzCknZtnFrW8")
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def scrape_for_data(account):

    extractor = twitter_setup()
    print("Searching for " + account)

    tweets = []
    # max_tweets = 10
    # searched_tweets = [status for status in tweepy.Cursor(extractor.search, q = account, since = "2019-2-19", until = "2019-2-21",  tweet_mode = "extended").items(max_tweets)]

    flag = True
    last_id = None
    while (flag):
        flag = False
        for status in tweepy.Cursor(extractor.search,
                                    q=account,
                                    since='2019-2-15',
                                    until = "2019-2-21",
                                    max_id=last_id,
                                    result_type='recent',
                                    include_entities=True,
                                    monitor_rate_limit=False,
                                    wait_on_rate_limit=True).items():
            tweet = status._json
            print(tweet)

            flag = True  # there still some more data to collect
            last_id = status.id  # for next time

    # for status in tweepy.Cursor(extractor.search, q = account, since = "2019-2-19", until = "2019-2-21",  tweet_mode = "extended").items(max_tweets):
    #     item = status.full_text.encode('utf-8').strip()
    #     time = status.created_at
    #     time = time - timedelta(hours=5)
    #     tweets.append([item, time])
    #     print(status)


    # c = tweepy.Cursor(extractor.search, q = account, since='2016-2-17',
                                                       #   until='2019-2-17', tweet_mode = "extended").items(max_tweets)
    # while True:
    #     try:
    #         tweet = c.next()
    #         item = tweet.full_text.encode('utf-8').strip()
    #         time = tweet.created_at
    #         time = time - timedelta(hours=5)
    #         tweets.append([item, time])
    #     except tweepy.TweepError:
    #         time.sleep(60 * 15)
    #         continue
    #     except StopIteration:
    #         break

    for tweet in searched_tweets:
        item = tweet.full_text.encode('utf-8').strip()
        time = tweet.created_at
        time = time - timedelta(hours = 5)
        tweets.append([item, time])
        print(tweet)

    data = pandas.DataFrame(tweets, columns=['Tweets', 'Times'])
    return data


def write_to_excel(account):

    data = scrape_for_data(account)
    with pandas.ExcelWriter("tweets.xlsx") as writer:
        data.to_excel(writer)

    writer.close()


if __name__ == "__main__":
    write_to_excel(input("Scrape for which Twitter account?"))
