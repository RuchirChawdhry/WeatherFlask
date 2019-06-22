import requests
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from model import *
from os import path, chdir
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/')
def weather():
    api_key_1 = "0e71adedcd098647c1ef46440888cb56"
    api_key_2 = "d7a597fef845c4a34a8604a08a589a15"
    api_key_3 = "1534719b67a41207d1af8b8c0fbde0d7"
    
    city = "Mumbai"

    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_2}&units=metric"

    data = requests.get(url).json()
    
    city_info = {
        "country" : data['sys']['country']
        "opw_id" : data['id']
        "cod" : data['cod']
        "timezone" : data['timezone']
    }

    weather_info = {
        "city" : city,
        "desc" : data['weather'][0]['description'],
        "temp" : data['main']['temp'],
        "temp_min" : data['main']['temp_min'],
        "temp_max" : data['main']['temp_max'],
        "pressure" : data['main']['pressure'],
        "humid" : data['main']['humidity'],
        "wind_speed" : data['wind']['speed'],
        "wind_deg" : data['wind']['deg'],
        "clouds" : data['clouds']
        "icon" : data[weather][0]['icon']
    }
    
    lat_long = {
        "latitude" : data['coord']['lat'],
        "longitude" : data['coord']['lon']
    }
    
    sun_info = {
        "sunrise" : data['sys']['sunrise'],
        "sunset" : data['sys']['sunset']
    }
    
    return weather_info
    return lat_long
    return sun_info
        

if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8000, debug=True)
    weather()
