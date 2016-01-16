from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse 
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
import models
from django.conf import settings
import os
import json
import time
import re
from lxml import etree
from lib import kookoo_lib
from lib import fb
from lib import twitter
from lib import load_data

def api_v1_main(request):
	if request.method=='GET':
		print request.GET
		#print request.GET['event']
		#POSSIBLE VALUES FOR "EVENT" PARAMETER
		#NewCall : When KooKoo receives a new call
		#Record : When KooKoo finishes recording a file
		#GotDTMF : When KooKoo has collected user input
		#Hangup : When the caller has hungup the current call
		#Disconnect: When we (KooKoo) disconnects the caller
		#Dial: When the outbound dial has finished
		#Conference: When the user terminates with # in the conference
		if 'event' not in request.GET:
			user_exist_demo= models.Call.objects.filter(sid= request.GET['sid']).exists()
			if user_exist_demo is True:
				#irst_response(message,is_text,sid=None,collectdtmf=False,format_lan=None,lang="EN",character_limit=1,terminal_character='#',timeout_time=1000)
				data= kookoo_lib.first_response(message='Press 1 to donate',is_text=True,sid=str(request.GET['sid']),collectdtmf=True)
				#time.sleep(3)
				return HttpResponse(data, content_type='application/xml' )		
		else:
			if request.GET['event']== 'NewCall':
				data= kookoo_lib.first_response(message='Welcome to tweet blood donoation IVR',is_text=True,format_lan=None)
				#ex: http://yourapp.com/ivr.php?event=NewCall&cid={caller id}&called_number={the number which was called}&sid={unique id of the call}&circle={telecom circle of the caller}&operator={the telecom operator of the caller}
				(new_call_save, new_call_save_status)= models.Call.objects.get_or_create(sid= request.GET['sid'], defaults={'circle': request.GET['circle'],'operator': request.GET['operator'],'cid': request.GET['cid'],'called_number':request.GET['called_number'],'event':str(request.GET['event'])})
				print 37
				print new_call_save
				print 39
				print new_call_save_status
				return HttpResponse(data, content_type='application/xml' )
				#<QueryDict: {u'called_number': [u'911130803946'], u'cid': [u'8041169706'], u'cid_e164': [u'+918041169706'], 
				#u'cid_type': [u'FIXED_LINE'], u'sid': [u'1104528084461170'], u'operator': [u'Airtel'], u'circle': [u'KARNATAKA'], 
				#u'event': [u'NewCall']}>
			elif request.GET['event']=='Hangup':
				data= kookoo_lib.first_response(message='Thanks for Calling tweet blood donoation IVR',is_text=True,format_lan=None)
				#{u'called_number': [u'911130803946'], u'cid': [u'8041169706'], u'process': [u'collectdtmf'], u'total_call_duration': [u'20'], u'sid': [u'9465281780016373'], u'event': [u'Hangup']}
				(hangup_save, hangup_status)= models.Hangup.objects.get_or_create(sid= request.GET['sid'], defaults={'total_call_duration':request.GET['total_call_duration'],'process':request.GET['process'],'cid': request.GET['cid'],'called_number':request.GET['called_number'],'event':str(request.GET['event'])})
				print 57
				print (hangup_save, hangup_status)
				print 59
				return HttpResponse(data, content_type='application/xml' )
			elif request.GET['event']=='Disconnect':
				data= kookoo_lib.first_response(message='Some Error Occured.Please try again',is_text=True,format_lan=None)
				(disconnect_save, disconnect_status)= models.Hangup.objects.get_or_create(sid= request.GET['sid'], defaults={'message':request.GET['message'],'total_call_duration':request.GET['total_call_duration'],'process':request.GET['process'],'cid': request.GET['cid'],'called_number':request.GET['called_number'],'event':str(request.GET['event'])})
				print 63
				print (disconnect_save, disconnect_status)
				print 35
				return HttpResponse(data, content_type='application/xml' )

			elif request.GET['event']=='GotDTMF':
				#event=GotDTMF&data={the digits entered by the caller}&sid={call id}
				if request.GET['data']=='1':
					data=kookoo_lib.first_response(message='1',is_text=False,format_lan='1',lang="EN")
				elif request.GET['data']=='2':
					data=kookoo_lib.first_response(message='2',is_text=False,format_lan='1',lang="EN")				
				return HttpResponse(data, content_type='application/xml' )
			else:
				data= kookoo_lib.first_response(message='Some Error Occured.Please try again',is_text=True,format_lan=None)
				return HttpResponse(data, content_type='application/xml' )

def api_v1_fb_parse(request):
	if request.method=='GET':
		print request.GET
		print settings.FACEBOOK_ACCESS_TOKEN
		dev_name=settings.FACEBOOK_ACCESS_TOKEN['dev_name']
		long_lived_access_token_exists= models.dev.objects.filter(dev_name= dev_name).exists()
		if long_lived_access_token_exists is False:

			long_live_access_token_dict=fb.get_long_access_token()
			(long_lived_access_token_save, long_lived_access_token_save_status)= models.dev.objects.update_or_create(dev_name=str(dev_name), defaults={'access_token': long_live_access_token_dict['long_lived_access_token'],'expiry_date': long_live_access_token_dict['expires_at']})
			print (long_lived_access_token_save, long_lived_access_token_save_status)
		get_long_lived_access_token= models.dev.objects.values('access_token').get(dev_name= dev_name)
		long_lived_access_token=get_long_lived_access_token['access_token']
		response_data={}
		print request.GET['fb_source'].split(',')
		for page in request.GET['fb_source'].split(','):
			page_data= fb.get_page_data(page,long_lived_access_token)
			print page_data
			(page_data_save, page_data_save_status)= models.Page.objects.update_or_create(page_id=str(page_data['id']), defaults={'page_name': page_data['name'],'likes': page_data['likes'],'talking_about_count': page_data['talking_about_count']})
			print (page_data_save, page_data_save_status)
			fb.get_posts_data(str(page_data['id']),long_lived_access_token)
			response_data[page]=True
		return HttpResponse(json.dumps(response_data), content_type="application/json")

def api_do_settings(request):		
	if request.method=='GET':		
		load_data.load_citydetails()		
		load_data.load_cityaliases()		
		load_data.load_bloodgroup_aliases()		
		return HttpResponse(json.dumps({'status':"Initial setup done"}), content_type="application/json")			
