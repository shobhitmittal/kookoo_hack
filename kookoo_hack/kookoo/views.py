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
from lib import data
from lxml import etree
# Create your views here.

#path_to_automation= '/home/shobhit/attivo/Attivo_Automation_Tools/automation_v2/'
#path_to_config= path_to_automation+'config'
#global_path= os.getcwd()

def api_v1_main(request):
	if request.method=='GET':
		print request.GET


		root = etree.Element('Response')
		#root.append(etree.Element('playtext'))
		# another child with text
		child = etree.Element('playtext')
		child.text = 'Hi helo'
		root.append(child)
		
		# pretty string
		s = etree.tostring(root, xml_declaration=True,encoding='utf-8')
		#print(etree.tostring(root, xml_declaration=True))
		print s

		#ex: http://yourapp.com/ivr.php?event=NewCall&cid={caller id}&called_number={the number which was called}&sid={unique id of the call}&circle={telecom circle of the caller}&operator={the telecom operator of the caller}
		return HttpResponse(s, content_type='application/xml' )