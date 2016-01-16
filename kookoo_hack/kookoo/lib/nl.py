import sys
import time
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz
import re

stop_words = stopwords.words('english')

tags=['bangalore','delhi']
blood_group=['A+','B+','o+','o +']
phone = ["9886295474", "+91-9883443344"]

def remove_stopwords(message):
	data_return=[]
	for message_token in message:
		if message_token not in stop_words:
			data_return.append(message_token)
	return data_return

def fuzzy_tagger(text,tags):
	selection=[]
	threshold=80
	for tag in tags:
		pr=fuzz.partial_ratio(text,tag)
		ts=fuzz.token_set_ratio(text,tag)
		if pr>threshold or ts>threshold:
			selection.append(tag)
	return selection

def find_tag(message,tags,blood_group,phone):
	message=gh.encode('utf-8').split()
	cleaned_message=remove_stopwords(message)
	print cleaned_message
	phone_regex = re.compile("^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$")
	
	place_list=[]
	blood_group_list=[]
	phone_number_list = []

	for j in cleaned_message:
		data_place=fuzzy_tagger(j,tags)
		if data_place:
			place_list.extend(data_place)
		data_blood=fuzzy_tagger(j,blood_group)
		if data_blood:
			blood_group_list.extend(data_blood)
		if phone_regex.match(j):
			phone_number_list.append(j)

	data_return={}
	data_return['place']=place_list
	data_return['blood_group']=blood_group_list
	data_return['phone'] = phone_number_list
	return data_return

if __name__ == '__main__':
	start=time.time()
	gh='RT @bld4needy: #Bangalore O+ve blood at Fortis Hospital, BTM Pls Call 9886295474 @BloodDonorsIn @iCanSaveLife @nistula @v_shakthi'
	print find_tag(gh,tags,blood_group,phone)
	print time.time()-start