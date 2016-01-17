from facepy.utils import get_extended_access_token
from facepy import GraphAPI
import json
from django.conf import settings
import nl
from kookoo import models
from django.db import transaction

@transaction.non_atomic_requests
def get_posts_data(page_id,access_token,tag_data_dict):
	graph = GraphAPI(access_token)
	#page_id= 'flipkart'
	data= graph.get(page_id+ "/posts?fields=id,created_time,updated_time,message,description&limit=100", page=True, retry=5)
	
	page_post= models.Page.objects.get(page_id= page_id)
	#transaction.set_autocommit(False)
	for i in data:
		#print i['data']
		for post_data in i['data']:
			print post_data
			if 'description' in post_data and 'message' in post_data:
				nl.nl_main_func(post_data['message'],tag_data_dict)
				nl.nl_main_func(post_data['description'],tag_data_dict)
				(post_data_save, post_data_save_status)= models.Posts.objects.update_or_create(post_id=str(post_data['id']), defaults={'page_id': page_post,'message': post_data['message'],'description': post_data['description'],'created_time': post_data['created_time'],'updated_time': post_data['updated_time']})
			elif 'description' not in post_data and 'message' in post_data:
				nl.nl_main_func(post_data['message'],tag_data_dict)
				(post_data_save, post_data_save_status)= models.Posts.objects.update_or_create(post_id=str(post_data['id']), defaults={'page_id': page_post,'message': post_data['message'],'created_time': post_data['created_time'],'updated_time': post_data['updated_time']})
			elif 'description' in post_data and 'message' not in post_data:
				nl.nl_main_func(post_data['description'],tag_data_dict)
				(post_data_save, post_data_save_status)= models.Posts.objects.update_or_create(post_id=str(post_data['id']), defaults={'page_id': page_post,'description': post_data['description'],'created_time': post_data['created_time'],'updated_time': post_data['updated_time']})
			else:
				pass
			print (post_data_save, post_data_save_status)
	#transaction.set_autocommit(True)
		#if i['data']:
		#	for j in i['data']:
		#		data_post_ids.append(j['id'])
	#print len(data_post_ids)

def get_page_data(page_id,access_token):
	graph=GraphAPI(access_token)
	data_page= graph.get(page_id+'?fields=likes,talking_about_count,id,name',retry=5)
	return data_page

def get_long_access_token():

	#application_secret_key='0840d857d5a2d153338f8f3197e6f597'
	#application_id='1685065455105239'
	#short_lived_access_token='CAAX8jtZCf9NcBABIaLBXiOB2vidhEcW5EHqGnyPonOxTSx0yxeqYUNeUwnsjHOiRM0SJF3Qq4CW7miia5eBFvcGgQkasyBRrkwZAoTcu40jq3OmgcUBEgFWVV3hGOe1p6EdBqM6SHSe0Yqn6Kbi2Kwf2J8eOuWjxgMUA9DiHZC65iGuZAyolihj1T3Lg0dwOohDcL60ZCCwv63PUvbfL7'
	application_secret_key=settings.FACEBOOK_ACCESS_TOKEN['app_secret']
	application_id=settings.FACEBOOK_ACCESS_TOKEN['app_id']
	short_lived_access_token=settings.FACEBOOK_ACCESS_TOKEN['short_lived_access_token']
	(long_lived_access_token, expires_at)= get_extended_access_token(short_lived_access_token, application_id, application_secret_key)
	print long_lived_access_token
	print expires_at
	#graph = GraphAPI(long_lived_access_token)
	#print graph.get('/me')
	data_to_return={}
	data_to_return['long_lived_access_token']=str(long_lived_access_token)
	data_to_return['expires_at']=str(expires_at)
	return data_to_return
