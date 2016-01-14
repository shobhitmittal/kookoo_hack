#from forms import testForm
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse 
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.conf import settings
import os
import json
import re
from lxml import etree
from lib import kookoo_lib
# Create your views here.

#path_to_automation= '/home/shobhit/attivo/Attivo_Automation_Tools/automation_v2/'
#path_to_config= path_to_automation+'config'
#global_path= os.getcwd()

def api_v1_main(request):
	if request.method=='GET':
		print request.GET
		print request.GET['event']
		#POSSIBLE VALUES FOR "EVENT" PARAMETER
		#NewCall : When KooKoo receives a new call
		#Record : When KooKoo finishes recording a file
		#GotDTMF : When KooKoo has collected user input
		#Hangup : When the caller has hungup the current call
		#Disconnect: When we (KooKoo) disconnects the caller
		#Dial: When the outbound dial has finished
		#Conference: When the user terminates with # in the conference
		if request.GET['event']== 'NewCall':

			data= kookoo_lib.first_response(message='Hi Press 1 to say 1.Press 2 to say 2',is_text=True,format_lan=None)
			#ex: http://yourapp.com/ivr.php?event=NewCall&cid={caller id}&called_number={the number which was called}&sid={unique id of the call}&circle={telecom circle of the caller}&operator={the telecom operator of the caller}
			return HttpResponse(data, content_type='application/xml' )


			#<QueryDict: {u'called_number': [u'911130803946'], u'cid': [u'8041169706'], u'cid_e164': [u'+918041169706'], 
			#u'cid_type': [u'FIXED_LINE'], u'sid': [u'1104528084461170'], u'operator': [u'Airtel'], u'circle': [u'KARNATAKA'], 
			#u'event': [u'NewCall']}>
		elif request.GET['event']=='Hangup':
			pass
		elif request.GET['event']=='GotDTMF':
			#event=GotDTMF&data={the digits entered by the caller}&sid={call id}
			if request.GET['data']=='1':
				data=kookoo_lib.first_response(message='1',is_text=False,format_lan=1,lang="EN")
			elif request.GET['data']=='2':
				data=kookoo_lib.first_response(message='2',is_text=False,format_lan=1,lang="EN")				
			return HttpResponse(data, content_type='application/xml' )
		else:
			data= kookoo_lib.first_response('Some Error Occured.Please try again')
			return HttpResponse(data, content_type='application/xml' )
