from django.db import models

class Call(models.Model):

	sid=models.CharField(max_length=255,primary_key=True)
	circle=models.CharField(max_length=255, unique=False)
	operator=models.CharField(max_length=255, unique=False)
	cid=models.CharField(max_length=255, unique=False)
	called_number=models.CharField(max_length=255, unique=False)
	event=models.CharField(max_length=255, unique=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
	#http://yourapp.com/ivr.php?event=NewCall&cid={caller id}&called_number={the number which was called}&
	#sid={unique id of the call}&circle={telecom circle of the caller}&operator={the telecom operator of the caller}

class Hangup(models.Model):
	
	sid=models.CharField(max_length=255,primary_key=True)
	total_call_duration=models.CharField(max_length=255, unique=False)
	process=models.CharField(max_length=255, unique=False)
	cid=models.CharField(max_length=255, unique=False)
	called_number=models.CharField(max_length=255, unique=False)
	event=models.CharField(max_length=255, unique=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
	#{u'called_number': [u'911130803946'], u'cid': [u'8041169706'],
	#u'process': [u'none'], u'total_call_duration': [u'13'], u'sid': [u'1104528084751171'], u'event': [u'Hangup']}