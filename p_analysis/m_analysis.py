import pandas as pd
from datetime import date
# Figures
import plotly
import plotly.express as px

def analyze():
    print('...lets read data with sentiment tweets...')
    data = pd.read_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/data_sentiment.csv')

    # select required columns
    data = data.drop(columns =['Unnamed: 0', 'Unnamed: 0.1'])
    print('...categorise tweets between today, yesterday, this month, last month...')

    # change date type from 'object' to 'date'
    data['date'] = pd.to_datetime(data['date'])

    data['month'] = data['date'].dt.to_period('M')
    data.head()

    # getting today's Timestamp
    today = pd.Timestamp.today().floor('D')
    # .normalize() does the same thing

    yesterday = today - pd.Timedelta(days=1)

    this_month = today.to_period('M').to_timestamp()

    this_month_name = pd.Timestamp.month_name(this_month)

    last_month = this_month - pd.Timedelta(days=30)

    last_month_name = pd.Timestamp.month_name(last_month)

    #greater than the start date and smaller than the end date
    yesterday_mask = (data['date'] > yesterday) & (data['date'] <= today)
    df_yesterday = data.loc[yesterday_mask]

    # today
    today_mask = (data['date'] > today)
    df_today = data.loc[today_mask]

    # this month
    this_month_mask = (data['date'] > this_month)
    df_this_month = data.loc[this_month_mask]

    #greater than the start date and smaller than the end date
    last_month_mask = (data['date'] >= last_month) & (data['date'] < this_month)
    df_last_month = data.loc[last_month_mask]

    sentiment_labels = ['very negative', 'negative', 'moderate', 'positive', 'very positive']
    print(f'...lets categorise the tweets according to their sentiment score:...{sentiment_labels}')

    df_score1 = (pd.cut(df_today['score_coded'] ,bins=[-1.0, -.60, -.20, .20, .60, 1.0] ,
                                labels=sentiment_labels).value_counts())

    df_score2 = (pd.cut(df_yesterday['score_coded'] ,bins=[-1, -.6, -.2, .2, .6, 1.0],
                                labels=sentiment_labels).value_counts())

    df_score3 = (pd.cut(df_this_month['score_coded'] ,bins=[-1, -.6, -.2, .2, .6, 1.0],
                                labels=sentiment_labels).value_counts())

    df_score4 = (pd.cut(df_last_month['score_coded'] ,bins=[-1, -.6, -.2, .2, .6, 1.0],
                                labels=sentiment_labels).value_counts())

    df_score = pd.DataFrame(columns = ['Today', 'Yesterday', this_month_name, last_month_name],
                       index = sentiment_labels)

    df_score['Today'] = df_score1
    df_score['Yesterday'] = df_score2
    df_score.iloc[:, 2] = df_score3
    df_score.iloc[:, 3] = df_score4
    df_score.rename_axis('Sentiment')

    df_score_fig = df_score.reset_index()
    df_score_fig.columns = ['sentiment', 'Today', 'Yesterday', this_month_name, last_month_name]
    print('...lets save the tweets together with their categorisation based on sentiment score...')

    df_score_fig.to_csv('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/data_sentiment_classified.csv', header=True)


    df_score_fig1= df_score_fig[['sentiment', 'Today', 'Yesterday']]
    df_score_fig2= df_score_fig[['sentiment', this_month_name, last_month_name]]


    # date = print(f"{today.day_name()} {today.day} {today.month_name()} {today.year}")


    fig1 = px.bar(df_score_fig1, x = 'sentiment', y = [df_score_fig1[i] for i in df_score_fig1.columns if i!='sentiment'], barmode='group',
                  title = f"@BiciMAD Tweets sentiments Today vs Yesterday\n{today.day_name()} {today.day} {today.month_name()} {today.year}",
                  labels = {"sentiment":"Sentiment", "value":"N. tweets",
                           'variable':"Day"})

    fig2 = px.bar(df_score_fig2, x = 'sentiment', y = [df_score_fig2[i] for i in df_score_fig2.columns if i!='sentiment'], barmode='group',
                  title = f"@BiciMAD Tweets sentiments Today vs Yesterday\n{today.day_name()} {today.day} {today.month_name()} {today.year}",
                  labels = {"sentiment":"Sentiment", "value":"N. tweets",
                  "variable": "Month"})
    print('figure is there!...')

    # htmkl file
    plotly.offline.plot(fig1, filename='/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/tweet_sentiment1.html')
    plotly.offline.plot(fig2, filename='/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/tweet_sentiment2.html')

    # png file
    fig1.write_image("/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/tweet_sentiment1.png")
    fig2.write_image("/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/tweet_sentiment2.png")
    print('figures saved in html and png!...')










