
def reporting():
	import requests
	import os
	print('...lets call the api again...')

	import tweepy


	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

	api = tweepy.API(auth, wait_on_rate_limit=True)
	print('api is with us!...')


	message = f'@BiciMAD status today'
	message

	images = ('/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/tweet_sentiment1.png', '/Users/Blanca/ironhack/gitrepo/ih_datamadpt0420_final_project/data/results/tweet_sentiment2.png')
	media_ids = [api.media_upload(i).media_id_string for i in images]
	tweet = api.update_status(status=message, media_ids=media_ids)
	print('TWEET has been posted!...')

