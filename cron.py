import requests
import time

while True:
	time.sleep(500)
	url='http://128.199.82.223/apiv1_fb_cron?twitter_source=Bloodhelpline,iCanSaveLife,BloodAid&fb_source=Blooddonors,bloodnetwork,BLOODFORSUREapp,RaktAbhaa'
	status_request= requests.get(url)
	time.sleep(3000)