import pandas as pd
import re

def analyze():
    data = pd.read_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/raw/rawdata.csv')
    print('...lets read the tweets saved...')
    # change date type from 'object' to 'date'
    data['date'] = pd.to_datetime(data['date'])
    # getting today's Timestamp
    today = pd.Timestamp.today().floor('D')
    # .normalize() does the same thing
    data = data[(data['date'] > today )]
    # select required columns
    data = data.drop(columns =['Unnamed: 0'])
    # data analysis => sorting
    data = data.sort_values('user_name', ascending=False)
    data = data[data.user_name != 'BiciMAD']
    data = data.reset_index()
    data = data.drop(columns =['index'])

    def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        #return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", tweet).split())
    print('...and clean them a bit...')

    # Updated the tweets_clean
    data['tweets_clean'] = data['text'].apply(clean_tweet)
    print('tweets cleaned!...')

    from transformers import pipeline
    classifier = pipeline('sentiment-analysis')
    from transformers import AutoTokenizer, AutoModelForMaskedLM
    tokenizer = AutoTokenizer.from_pretrained("dccuchile/bert-base-spanish-wwm-cased")
    model = AutoModelForMaskedLM.from_pretrained("dccuchile/bert-base-spanish-wwm-cased")
    print('...sentiment analysis model from transformers there...')

    def transform (x):
        return classifier(x)
    # Apply transform function to all tweets
    data['sentiment']=data['tweets_clean'].apply(transform)
    print('TODAYs tweets with sentiment analysis done!...')

    data["score"] = [data["sentiment"][i][0]['score'] for i in range(data.shape[0])]
    data["label"] = [data["sentiment"][i][0]['label'] for i in range(data.shape[0])]
    score = data['score']
    positive = (data["label"] == "POSITIVE")
    negative = (data["label"] == "NEGATIVE")
    data['label_coded'] = data['label'].apply(lambda x: 1 if x == 'POSITIVE' else -1)
    data['score_coded'] = data['label_coded'] * data['score']
    df_old = pd.read_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/data_sentiment.csv')
    df_old = df_old.astype(str)
    df_str = data.astype(str)
    df = pd.merge(df_old, df_str, how='outer')
    df = df[df.date != 'date']
    df.drop_duplicates(subset=['id'], keep='last', inplace=True)
    df.reset_index()
    # check new Tweets are in df
    df.sort_values('date', ascending=False).head(10)
    # save to csv - add a dataframe to an existing csv file
    df.to_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/data_sentiment.csv', header=True)
    print('TODAYs tweets with sentiment label and score saved!...')













