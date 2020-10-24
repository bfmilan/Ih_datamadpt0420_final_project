

import datetime

import pandas as pd
search_term = 'BiciMAD'

# Creation of query method using parameters
# tweets = tweepy.Cursor(api.user_timeline,id=username).items(count)
tweets = tweepy.Cursor(api.search, 
                   q=search_term,
                   lang="es", tweet_mode="extended", since=datetime.datetime.today().strftime('%Y-%m-%d')).items()
 
tweets_list = [[tweet.created_at, tweet.id, tweet.full_text, tweet.user.name, tweet.user.id, tweet.user.screen_name] for tweet in tweets]

# Creation of dataframe from tweets list
# Add or remove columns as you remove tweet information
tweets_df = pd.DataFrame(tweets_list)



    
df_tweets = tweets_df.copy()

# Rename columns
df_tweets.set_axis(['date','id', 'text', 'user_name','user_id', 'user_screen_name'], axis=1, inplace=True)
# Drop duplicates before sav
# Read alrady existing data 
df_old = pd.read_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/raw/rawdata.csv')
df_old = df_old.drop(columns =['Unnamed: 0'])
df_old = df_old.astype(str)
df_str = df_tweets.astype(str)
df = pd.merge(df_old, df_str, how ='outer')
df = df[df.date != 'date']
df.drop_duplicates(subset=['id'],keep='last', inplace= True)
df.reset_index()

# check new Tweets are in df
df.sort_values('date', ascending = False).head(10)

# save to csv - add a dataframe to an existing csv file
df.to_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/raw/rawdata.csv', header=True)
