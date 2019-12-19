# curl -k -X GET --header "Accept: application/json" 
# --header "Authorization: Bearer 17965aae3198d1f3a99357237de9b3c2" 
# https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/8101

import requests
from datetime import datetime
import base64


key = "xbBJvXN10rIiYjYJEg6E0lG9xu0a"
secret = "ZdvKc8aW1R0P5ZEZw_Y_f3Gbzuga"
token = ""

def regenerate_token():
	#curl -k -d "grant_type=client_credentials" -H "Authorization: Basic BASE64KEY+:+SECRET" https://opendata-api.stib-mivb.be/token
	#Put your Consumer Key and Secret key in the following format: << YouConsumerKey:YouSecretKey >> and convert it to Base64 
	#In the command, replace BASE64KEY+:+SECRET by the two converted keys.

	# this works :
	# oscar@oscar-is-back ~/Projets/balena-sense/stib/scripts $ curl -k -d "grant_type=client_credentials" -H "Authorization: Basic eGJCSnZYTjEwcklpWWpZSkVnNkUwbEc5eHUwYTpaZHZLYzhhVzFSMFA1WkVad19ZX2YzR2J6dWdh" https://opendata-api.stib-mivb.be/token
	# "access_token":"d5d5f96a3c4fb9ee3d9ad96c441fe15b","scope":"am_application_scope default","token_type":"Bearer","expires_in":2293}

	keysecret = "%s:%s" %(key, secret)
	keysecret64 = base64.b64encode(keysecret.encode("utf-8"))
	url = "https://opendata-api.stib-mivb.be/token"
	payload = {
		'grant_type' : 'client_credentials' 
	}
	headers = {'Authorization': 'Basic %s'%(keysecret64)}
	r = requests.post(url, data=payload, headers=headers)
	if r.status_code == 200:
		return r.json()["access_token"]


url = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/8101'
token = regenerate_token()
headers = {'Accept': 'application/json', 'Authorization': 'Bearer %s'%token}
# r = requests.post(url, data=payload, headers=headers)
r = requests.get(url, headers=headers)
if r.status_code == 200	:
	for p in r.json()["points"]:
		for t in p["passingTimes"] :
			d = t["expectedArrivalTime"] #
			date_time_obj = datetime.strptime(d, '%Y-%m-%dT%H:%M:%S+01:00')
			diff = date_time_obj- datetime.now()
			print diff.seconds / 60