from kookoo import models
import time
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
import re
import string

punctuation_remove='!"#$%&\'()*,./:;<=>?@[\\]^_`{|}~'
phone_regex = re.compile("^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$")
stop_words = stopwords.words('english')
stop_words.extend(['blood','bank','hospital','nagar','urgent','hosp','call','metro','need'])
blood_group={'a+':['a+','a +','a +ve','a+ve'],'b+':['b+','b +','b +ve','b+ve'],'a-':['a-','a -','a -ve','a-ve'],'b-':['b-','b -','b -ve','b-ve'],'o+':['o+','o +','o +ve','o+ve'],'o-':['o-','o -','o -ve','o-ve'],'ab+':['ab+','ab +','ab +ve','ab+ve'],'ab-':['ab-','ab -','ab -ve','ab-ve']}
phone = ["9886295474", "+91-9883443344"]

def remove_punctuation(message):
	start=time.time()
	for pun in punctuation_remove:
		message=message.replace(pun,'')
	print 'punctuation ',time.time()-start
	return message

def remove_stopwords(message):
	start=time.time()
	data_return=[]
	for message_token in message:
		if message_token not in stop_words:
			data_return.append(message_token)
	print 'STOPWORDS ',time.time()-start
	return data_return

def fuzzy_tagger(text,tags,isblood=False):
	selection=[]
	threshold=95
	for tag in tags:
		if isblood is False:
			if abs(len(tag) -len(text)) <= 2:
				if text==tag:
				#pr=fuzz.partial_ratio(text,tag)
				#ts=fuzz.token_set_ratio(text,tag)
				#if pr>threshold or ts>threshold:
					selection.append(tag)
		else:
			if text==tag:
			#pr=fuzz.partial_ratio(text,tag)
			#ts=fuzz.token_set_ratio(text,tag)
			#if pr>threshold or ts>threshold:
				selection.append(tag)
	return selection

def find_tag(message,tags,blood_group):
	message=message.encode('utf-8').lower()
	message=remove_punctuation(message)
	message=message.split()
	message= list(set(message))
	cleaned_message=remove_stopwords(message)
	print cleaned_message
	
	place_list=[]
	blood_group_list=[]
	phone_number_list = []

	flag_blood_found=False
	flag_phone_found=False

	start=time.time()
	for jj in cleaned_message:
		#print blood_group
		data_blood=fuzzy_tagger(jj,blood_group,isblood=True)
		if data_blood:
			blood_group_list.extend(data_blood)
			flag_blood_found=True
			cleaned_message.remove(jj)
		if phone_regex.match(jj):
			phone_number_list.append(jj)
			flag_phone_found=True
			cleaned_message.remove(jj)
	print 'BLOOD_PHONE ',time.time()-start

	if flag_blood_found is True and flag_phone_found is True:
		start_1=time.time()
		for j in cleaned_message:
			print 41
			if len(j)>3:
				start=time.time()
				data_place=fuzzy_tagger(j,tags)
				print 43,j
				if data_place:
					place_list.extend(data_place)
				print 'CITY ',time.time()-start
		print 'PLACE ',time.time()-start_1

	data_return={}
	data_return['place']=place_list
	data_return['blood_group']=blood_group_list
	data_return['phone'] = phone_number_list
	return data_return


def nl_main_func(message,post_id,place_dict):
	place_dict_keys= place_dict.keys()
	blood_group_cleaned =[]
	for blood_group_cleaned_element in blood_group.values():
		blood_group_cleaned.extend(blood_group_cleaned_element)
	data_tag= find_tag(message,place_dict_keys,blood_group_cleaned)
	print data_tag
	post_id= models.Posts.objects.get(post_id= post_id)
	
	for place_data in data_tag['place']:
		place_obj= models.Places.objects.get(place= place_data)
		for blood_data in data_tag['blood_group']:
			for blood_key in blood_group.keys():
				if blood_data in blood_group[blood_key]:
					blood_data_main= blood_key
			for phone_number_data in data_tag['phone']:
				(tag_data_save, tag_data_save_status)= models.Tag_table.objects.update_or_create(post_id=post_id,place=place_obj,phone=phone_number_data,blood_group=blood_data_main,unit_req='5')
				print (tag_data_save, tag_data_save_status)