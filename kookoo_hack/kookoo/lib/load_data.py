from facepy.utils import get_extended_access_token
from facepy import GraphAPI
import json
from django.conf import settings
from kookoo import models
import csv
import os
from django.db import transaction

@transaction.non_atomic_requests
def load_citydetails():
	csv_data_path = str(os.getcwd()) + "/kookoo/data/all_india_pincode_circle.csv"
	with open(csv_data_path, 'rb') as csvfile:
		place_reader = csv.reader(csvfile, delimiter=',')
		count = 0
		for row in place_reader:
			telecom_circle  = str(row[-1]).lower().strip().lstrip().rstrip()
			for place_names in row:
				name_field = str(place_names).lower().strip().lstrip().rstrip()
				print name_field, count
				try:
					(name_data_save, name_data_save_status) = models.Places.objects.update_or_create(place = str(name_field), defaults = {'telecom_circle': str(telecom_circle)})
					print (name_data_save, name_data_save_status)
					count += 1
				except Exception as ex:
					print str(ex)

def load_cityaliases():
	csv_data_path = str(os.getcwd()) + "/kookoo/data/city_mappings.csv"
	with open(csv_data_path, 'rb') as csvfile:
		place_reader = csv.reader(csvfile, delimiter=',')
		count = 0
		for row in place_reader:
			place_alias  = str(row[1]).lower().strip().lstrip().rstrip()
			name_field = str(row[0]).lower().strip().lstrip().rstrip()
			print name_field, count
			try:
				(name_data_save, name_data_save_status) = models.Place_aliases.objects.update_or_create(alias = str(place_alias), defaults = {'place': str(name_field)})
				print (name_data_save, name_data_save_status)
				count += 1
			except Exception as ex:
				print str(ex)

def load_bloodgroup_aliases():
	csv_data_path = str(os.getcwd()) + "/kookoo/data/blood_group.csv"
	with open(csv_data_path, 'rb') as csvfile:
		place_reader = csv.reader(csvfile, delimiter=',')
		count = 0
		for row in place_reader:
			group  = str(row[0]).lower().strip().lstrip().rstrip()
			alias = str(row[1]).lower().strip().lstrip().rstrip()
			print alias, count
			try:
				(group_data_save, group_data_save_status) = models.Blood_group.objects.update_or_create(alias = str(alias), group = str(group))
				print (group_data_save, group_data_save_status)
				count += 1
			except Exception as ex:
				print str(ex)