import tweepy
CONSUMER_KEY = 'ithbpbVbiUJArSNYKsfGBXxWY'
CONSUMER_SECRET = 'aMxdR6o1cnMLeIOMyyhMiGKOlHAPatftLsEJwdnGAZgUaE0bM0'
ACCESS_TOKEN = '1270360148-YZ023UzKeg6JDVnbfsSjpjWQahwVrjz2ScrFwB3'
ACCESS_SECRET = 'P2VSHnA70K2rFEYpgDJ38I4q1Sn74XICqqHuGqnEWGlOv'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

import pandas as pd

search_term = 'BiciMAD'

try:     
 # Creation of query method using parameters
    # tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
    tweets = tweepy.Cursor(api.search,
                   q=search_term,
                   lang="es").items(1000)
 
    tweets_list = [[tweet.created_at, tweet.id, tweet.text, tweet.user.name] for tweet in tweets]
 
 # Creation of dataframe from tweets list
 # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list)
except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
    
df_tweets = tweets_df.copy()

# Rename columns
df_tweets.set_axis(['date','id', 'text', 'user_name'], axis=1, inplace=True)
# Drop duplicates before sav
# Read alrady existing data 
df_old = pd.read_csv('../data/raw/rawdata.csv')
df_old = df_old.drop(columns =['Unnamed: 0'])
df_old = df_old.astype(str)

df = pd.merge(df_old, df_str, how ='outer')
df = df[df.date != 'date']
df.drop_duplicates(subset=['id'],keep='last', inplace= True)
df.reset_index()

# save to csv - add a dataframe to an existing csv file
df.to_csv('./../data/raw/rawdata.csv', header=True)
