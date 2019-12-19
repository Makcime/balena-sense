import sys
import os
import json

from http.server import HTTPServer, BaseHTTPRequestHandler

import requests
from datetime import datetime
import base64

class stibMivb():

    def __init__(self):
        self.token = self.regenerate_token()
        self.retry = 0

    def regenerate_token(self):
        key = "xbBJvXN10rIiYjYJEg6E0lG9xu0a"
        secret = "ZdvKc8aW1R0P5ZEZw_Y_f3Gbzuga"
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
        else :
            return ""

    def get_waiting_time(self):
        url = 'https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/8101'
        headers = {'Accept': 'application/json', 'Authorization': 'Bearer %s'%self.token}
        # r = requests.post(url, data=payload, headers=headers)
        l = []
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            self.token = self.regenerate_token()
            l = [0, 0]
        else :
            for p in r.json()["points"]:
                for t in p["passingTimes"] :
                    d = t["expectedArrivalTime"] #
                    date_time_obj = datetime.strptime(d, '%Y-%m-%dT%H:%M:%S+01:00')
                    diff = date_time_obj- datetime.now()
                    l.append( int((diff.seconds / 60) - 60))

        return [
            {
                'measurement': 'stib-mvib',
                'fields': {
                    'waiting_A': l[0],
                    'waiting_B': l[1]
                }
            }
        ]


class stibMivbHTTP(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        waiting_times = stib.get_waiting_time()
        self.wfile.write(json.dumps(waiting_times[0]['fields']).encode('UTF-8'))

    def do_HEAD(self):
        self._set_headers()


# Start the server to answer requests for readings
stib = stibMivb()

while True:
    server_address = ('', 80)
    httpd = HTTPServer(server_address, stibMivbHTTP)
    print('Stib HTTP server running')
    httpd.serve_forever()

