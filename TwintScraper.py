import twint

c = twint.Config()

c.Search = "@Apple"
c.Verified = True
c.Lang = "en"
c.Store_csv = True
c.Output = "AppleTweets.csv"
c.Since = "2019-01-01"
c.Until = "2019-01-11"
c.Custom["tweet"] = ["username", "date", "time", "tweet"]

twint.run.Search(c)
