from facepy.utils import get_extended_access_token
from facepy import GraphAPI
import json
import timeit
from django.conf import settings

def get_posts_data(page_id,access_token):
#start = timeit.default_timer()

#access = 'CAACEdEose0cBAHecnhS2vvE6G2bcwkFZCWQEWoqdAYVLpFwD8BrJ6UyDPKYnhsqA27b2jCyngYXnKLvl8X8PhNyFuVF5zIBMZBVlzkUtDWlPgsDdexVNNZCf4AoyEWna5vyPiO16XIiZAvm0SFdfmnmSEHWxysFELnuONtc3o8f7ELWOcjTedDMdrzlYpa5JzHJ2vNeLNUju9ZA4jpa40'

graph = GraphAPI(access_token)
#page_id= 'flipkart'
data= graph.get(page_id+ "/posts?fields=id,message&limit=250", page=True, retry=5)


for i in data:
	print i['data']
	if i['data']:
		for j in i['data']:
			data_post_ids.append(j['id'])
#print len(data_post_ids)

def get_long_access_token():

	#application_secret_key='0840d857d5a2d153338f8f3197e6f597'
	#application_id='1685065455105239'
	#short_lived_access_token='CAAX8jtZCf9NcBABIaLBXiOB2vidhEcW5EHqGnyPonOxTSx0yxeqYUNeUwnsjHOiRM0SJF3Qq4CW7miia5eBFvcGgQkasyBRrkwZAoTcu40jq3OmgcUBEgFWVV3hGOe1p6EdBqM6SHSe0Yqn6Kbi2Kwf2J8eOuWjxgMUA9DiHZC65iGuZAyolihj1T3Lg0dwOohDcL60ZCCwv63PUvbfL7'
	application_secret_key=settings.app_secret
	application_id=settings.app_id
	short_lived_access_token=settings.short_lived_access_token
	long_lived_access_token, expires_at = get_extended_access_token(short_lived_access_token, application_id, application_secret_key)
	print long_lived_access_token
	print expires_at
	graph = GraphAPI(long_lived_access_token)
	print graph.get('/me')