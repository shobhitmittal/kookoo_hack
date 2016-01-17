import tweepy
from kookoo import models
from django.conf import settings
from django.db import transaction
import nl

consumer_key=settings.TWITTER_ACCESS_TOKEN['consumer_key']
consumer_secret=settings.TWITTER_ACCESS_TOKEN['consumer_secret']
access_token=settings.TWITTER_ACCESS_TOKEN['access_token']
access_token_secret=settings.TWITTER_ACCESS_TOKEN['access_token_secret']

def fetch_twitter_id(tweet_handle):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	api = tweepy.API(auth)
	handle_id=api.get_user(screen_name=str(tweet_handle))
	data_to_return={}
	data_to_return['id']=str(handle_id.id)
	data_to_return['follower_count']=handle_id.followers_count
	return data_to_return

@transaction.non_atomic_requests
def fetch_twitter_post(handle_id,tag_data_dict):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	api = tweepy.API(auth)
	page_post= models.Page.objects.get(page_id= handle_id)
	for status in tweepy.Cursor(api.user_timeline,id=handle_id,count=200,exclude_replies=True).items(4000):
	    (tweet_data_save, tweet_data_save_status)= models.Posts.objects.update_or_create(post_id=str(status.id), defaults={'page_id': page_post,'message': str(status.text.encode('utf-8')),'created_time': str(status.created_at),'updated_time': str(status.created_at)})
	    nl.nl_main_func(str(status.text.encode('utf-8')),str(status.id),tag_data_dict)
	    print (tweet_data_save, tweet_data_save_status)