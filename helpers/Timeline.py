import tweepy
import pandas as pd


class Timeline:
    def __init__(self, auth_data):
        # extract keys
        self.consumer_key = auth_data['consumer']['key']
        self.consumer_secret = auth_data['consumer']['secret']
        self.access_key = auth_data['access']['key']
        self.access_secret = auth_data['access']['secret']

    def load_tweets(self, screen_name):  # uses api to load tweets for a certain screen name

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)

        # used to get dicts from status object
        def get_json(status): return status._json
        # so it can be directly inserted into pd dataframe
        tweets = pd.DataFrame(
            list(map(get_json, api.user_timeline(screen_name=screen_name, count=200))))
        # using a lambda as a shorthand for api call, i'm honestly so sorry for this

        def get_next_200(max_id): return list(map(get_json, api.user_timeline(
            screen_name=screen_name, count=200, max_id=max_id)))
        # is 0 if all tweets loaded
        load_len = len(tweets)
        while load_len > 0:
            try:  # for connectivity issues causing exceptions, or api limits
                # getting id of last tweet in data frame
                max_id = tweets.iloc[-1].id - 1
                # loading 200 tweets that are older than my oldest tweet (max_id)
                load = get_next_200(max_id)
                load_len = len(load)  # update
                tweets = tweets.append(pd.DataFrame(load))
                total = len(tweets)

                # remove for less verbosity
                print("collected {} tweets. ".format(total))
            except:
                break

        tweets.to_csv('{}_tweets.csv'.format(screen_name),
                      encoding='utf-8')  # save data as csv file
        return tweets
