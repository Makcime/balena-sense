import json

apikey="key_redacted" # sign up here http://www.wunderground.com/weather/api/ for a key

url="http://api.wunderground.com/api/"+apikey+"/conditions/q/UK/Basingstoke.json"
meteo=urlopen(url).read()
meteo = meteo.decode('utf-8')
weather = json.loads(meteo)

for key, value in weather['current_observation'].items():
    print (key, value)