import re
import json
import redis
import requests
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_weather(request):

    scode = request.GET.get('scode', None)
    if scode == None:
        response = {
            "status": False,
            "message": "Invalid URL!"
        }
        return Response(response)

    nocache = request.GET.get('nocache', None)
    if nocache != None:
        nocache = int(nocache)    
        if nocache != 1:
            response = {
                "status": False,
                "message": "Invalid URL!"
            }
            return Response(response)
        

    # connecting to redis
    r = redis.Redis('localhost')    
    print(r.keys())

    data = r.get(scode)

    if data is not None and nocache != 1:
        return Response(json.loads(data)) # returning the data we got from the cache

    url = "https://tgftp.nws.noaa.gov/data/observations/metar/stations/"+scode+".TXT"

    report = requests.get(url, timeout=5, verify=False) # getting station report from the url

    if report.status_code == 404: # if scode is invalid
        response = {
            "status": False,
            "message": "Invalid URL!"
        }
        return Response(response)

    data = report.text
    data = re.split(r'[\n ]', data) 

    last_observation = get_last_observation(data)
    temperature = get_temperature(data[2:])
    wind = get_wind(data)

    
    response = {
        "data":{
            "station": scode,
            "last_observation": last_observation,
            "temperature": temperature,
            "wind": wind
        }
    }

    # storing in the cache 
    r.set(scode, json.dumps(response))
    r.expire(scode, timedelta(minutes=5)) # key expiry

    return Response(response)
    

def get_last_observation(data):
    """
    This function returns the last observation(date, time) from the data.
    """
    date, time = data[0], data[1]
   
    last_observation = "{} at {} GMT".format(date, time)
    return last_observation

def get_wind(data):
    '''
    This function returns wind speed from the data. If knots is not available in the data, then it returns "N/A"
    '''
    knots = ''
    for i in data:
        if "KT" in i:
            knots = i
    
    knots = knots.split('K')[0][-2:]
    
    try:
        knots = int(knots[:2])
    except ValueError:
        return "N/A"

    mph = round(knots * 1.151) # formula to get mph from knots
    wind = "S at {} mph ({} knots)".format(mph, knots) 
    return wind

def get_temperature(data):
    """
    This function returns temperature from the data. if celcius is not available in the data, then it returns "N/A"
    """
    celcius = 0
    celcius = [i for i in data if re.search(r'\d+[/]', i)]
    
    if celcius == []:
        return "N/A"
    celcius = celcius[0].split('/')[0]
    celcius = celcius.replace('M', '-')
      
    try:
        celcius = int(celcius)
    except ValueError:
        return "N/A"

    farenheit = round((celcius * 9/5) + 32) # formula to get farenheit from celcius
    temperature = "{0} C ({1} F)".format(celcius, farenheit)
    return temperature