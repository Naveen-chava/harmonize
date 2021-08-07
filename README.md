# Harmonize
Harmonize take home assignment

# Steps to setup & run

### Clone the repo
```
git clone https://github.com/Naveen-chava/harmonize.git
```
### Install virtualenv
```
pip3 install virtualenv
```
or
```
sudo apt install virtualenv
```
### Create and Activate the virtualenv
```
virtualenv env_name
sourve env_name/bin/activate
```
### Install the requirements
```
pip3 install -r requirements.txt
```

### Install redis-server
```
sudo apt install redis-server
```

### Run the server
```
python3 manage.py runserver
```

## API Endpoints
```
http://127.0.0.1:8000/metar/info?scode=<station_code>
http://127.0.0.1:8000/metar/info?scode=<station_code>&nocache=1
```
station_code is a valid station code. All the valid station codes are available [here](https://tgftp.nws.noaa.gov/data/observations/metar/stations/)

### Sample Request
Here the request body is empty.
```
http://127.0.0.1:8000/metar/info?scode=BARK
```
or
```
http://127.0.0.1:8000/metar/info?scode=BARK&nocache=1
```
When a request is made for a particular station, the response will be stored in cache for upto 5 minutes. nocache=1 parameter is optional. If it is used, the live data will be fetched and the cache will be updated.

### Sample Response
```
{
    "data": {
        "station": "BARK",
        "last_observation": "2019/07/03 at 09:00 GMT",
        "temperature": "37 C (99 F)",
        "wind": "S at 9 mph (8 knots)"
    }
}
```
