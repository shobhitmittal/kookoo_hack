from facepy import GraphAPI
import json
import timeit

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