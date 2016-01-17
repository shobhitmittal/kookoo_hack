# kookoo_hack

Deploy it on a Server

Enter the relevant data in kookoo_hack/kookoo_hack/settings_server.py
<code>
FACEBOOK_ACCESS_TOKEN={'dev_name':'','app_id':'',
'short_lived_access_token':''}

TWITTER_ACCESS_TOKEN={'consumer_key':'','consumer_secret':'',
'access_token':'','access_token_secret':''}
</code>

Change 
<code>os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kookoo_hack.settings")</code>
to
<code>os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kookoo_hack.settings_server")</code>

To run
<code>sudo bash setup_server.sh</code>
<code>bash run.sh</code>