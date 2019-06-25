import requests
from flask import Flask, render_template, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from model import *
from os import path, chdir
from datetime import date, datetime
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, DataRequired

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Login form fields (flask_wtf & wtforms)
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max = 49)] )
    remember = BooleanField('Remember Me')

# Register form fields (flask_wtf & wtforms)    
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=49)])
    email = StringField('email', validators=[InputRequired(), Email(message="invalid email"), Length(max=49)])

# Table that stores the immediate weather report of the city queried
class cityToday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cityName = db.Column(db.String(50))
    cityDesc = db.Column(db.String(30))
    cityTemp = db.Column(db.String(30))
    cityTempMin = db.Column(db.String(30))
    cityTempMax = db.Column(db.String(30))
    cityPressure = db.Column(db.String(30))
    cityHumid = db.Column(db.String(30))
    cityWindSpeed = db.Column(db.String(30))
    cityWindDeg = db.Column(db.String(30))
    cityClouds = db.Column(db.String(50))
    cityIcon = db.Column(db.String(30))
    cityLat = db.Column(db.Integer)
    cityLong = db.Column(db.Integer)
    citySunrise = db.Column(db.Integer)
    citySunset = db.Column(db.Integer)
    
    def __repr__(self):
        return f"<cityToday {cityName}>"

# Table that stores weather forecast report of the city queried
class cityForecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.Integer)
    cityName = db.Column(db.String(50))
    cityTemp = db.Column(db.Integer)
    cityTempMin = db.Column(db.Integer)
    cityTempMax = db.Column(db.Integer)
    cityPressure = db.Column(db.Integer)
    cityHumid = db.Column(db.Integer)
    cityWindSpeed = db.Column(db.Integer)
    cityWindDeg = db.Column(db.Integer)
    cityClouds = db.Column(db.String(50))
    cityIcon = db.Column(db.String(30))
    cityRain = db.Column(db.String(50))
    cityDesc = db.Column(db.String(30))
    cityDateTime = db.Column(db.String(50))


    def __repr__(self):
        return
    
db.create_all()

# @app.route('/')
# def index():
#     return render_template('index.html')

class Weather:
    @app.route('/weather')
    def weather():
        api_key_1 = "0e71adedcd098647c1ef46440888cb56"
        api_key_2 = "d7a597fef845c4a34a8604a08a589a15"
        api_key_3 = "1534719b67a41207d1af8b8c0fbde0d7"
        
        city = "Mumbai"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_2}&units=metric"

        data = requests.get(url).json()
        
        city_info = {
            "country" : data['sys']['country'],
            "opw_id" : data['id'],
            "cod" : data['cod'],
            "timezone" : data['timezone']
        }

        weather_info = {
            "cityName" : city,
            "cityDesc" : data['weather'][0]['description'],
            "cityTemp" : data['main']['temp'],
            "cityTempMin" : data['main']['temp_min'],
            "cityTempMax" : data['main']['temp_max'],
            "cityPressure" : data['main']['pressure'],
            "cityHumid" : data['main']['humidity'],
            "cityWindSpeed" : data['wind']['speed'],
            "cityWindDeg" : data['wind']['deg'],
            "cityClouds" : data['clouds']['all'],
            "cityIcon" : data['weather'][0]['icon']
        }
        
        lat_long = {
            "cityLat" : data['coord']['lat'],
            "cityLong" : data['coord']['lon']
        }
        
        sun_info = {
            "citySunrise" : data['sys']['sunrise'],
            "citySunset" : data['sys']['sunset']
        }
        
        # combined_dict = {**weather_info, **lat_long, **sun_info}

        weather = cityToday(**weather_info, **lat_long, **sun_info)
        
        db.session.add(weather)
        db.session.commit()
        
        return render_template('index.html')

class Forecast():
    @app.route('/forecast')
    def forecast():
        api_key_1 = "0e71adedcd098647c1ef46440888cb56"
        api_key_2 = "d7a597fef845c4a34a8604a08a589a15"
        api_key_3 = "1534719b67a41207d1af8b8c0fbde0d7"
        
        city_id = "1275339"

        url = f"https://api.openweathermap.org/data/2.5/forecast?id={city_id}&appid={api_key_2}&units=metric"

        data = requests.get(url).json()
        cleaner_data = data["list"]
        
        for i in range(len(cleaner_data)):
            try:
                forecast_dict = {
                    "dt" : cleaner_data[i]['dt'],
                    "cityName" : "empty",
                    "cityTemp" : cleaner_data[i]['main']['temp'],
                    "cityTempMin" : cleaner_data[i]['main']['temp_min'],
                    "cityTempMax" : cleaner_data[i]['main']['temp_max'],
                    "cityPressure" : cleaner_data[i]['main']['pressure'],
                    "cityHumid" : cleaner_data[i]['main']['humidity'],
                    "cityWindSpeed" : cleaner_data[i]['wind']['speed'],
                    "cityWindDeg" : cleaner_data[i]['wind']['deg'],
                    "cityClouds" : cleaner_data[i]['clouds']['all'],
                    "cityIcon" : cleaner_data[i]['weather'][0]['icon'],
                    "cityRain" : cleaner_data[i]['rain']['3h'],
                    "cityDesc" : cleaner_data[i]['weather'][0]['description'],
                    "cityDateTime" : cleaner_data[i]['dt_txt']
                }
                forecast = cityForecast(**forecast_dict)
                db.session.add(forecast)

            except KeyError:
                forecast_dict = {
                    "dt" : cleaner_data[i]['dt'],
                    "cityName" : "empty",
                    "cityTemp" : cleaner_data[i]['main']['temp'],
                    "cityTempMin" : cleaner_data[i]['main']['temp_min'],
                    "cityTempMax" : cleaner_data[i]['main']['temp_max'],
                    "cityPressure" : cleaner_data[i]['main']['pressure'],
                    "cityHumid" : cleaner_data[i]['main']['humidity'],
                    "cityWindSpeed" : cleaner_data[i]['wind']['speed'],
                    "cityWindDeg" : cleaner_data[i]['wind']['deg'],
                    "cityClouds" : cleaner_data[i]['clouds']['all'],
                    "cityIcon" : cleaner_data[i]['weather'][0]['icon'],
                    "cityRain" : 'not_found',
                    "cityDesc" : cleaner_data[i]['weather'][0]['description'],
                    "cityDateTime" : cleaner_data[i]['dt_txt']
                }
                
                forecast = cityForecast(**forecast_dict)
                db.session.add(forecast)
                
        db.session.commit()
        print(**forecast_dict)
                
        return render_template('index.html')

# Testing page to test jinja template:
@app.route('/func.html')
def func():
    def forecaster():
        return "testing"
    return render_template("func.html", weatherinfo = Weather.weather_info)

@app.route('/')
def index():
    return render_template('index.html')

# TODO: NEED TO COMPLETE THE CITYLIST ROUTE & FUNCTIONALITY
@app.route('/citylist')
def citylist():
    THIS_FOLDER = path.dirname(path.abspath(__file__))
    df = pd.read_json(THIS_FOLDER+"/city.list.json")
    df = df.to_html()
    # print(df)
    return df.to_html()
    return render_template("citylist.html")


# @app.route('/citylist')
# def citylist_():
#     return render_template("citylist.html")

# The login route. Posts data to users table if the data passes the validation tests.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        return form.username.data + form.password.data
    
    return render_template("login.html", form=form)

# The registration route. Posts data to users table if the data passes the validation tests.
@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        return form.username.data + form.email.data + form.password.data
    
    return render_template("register.html", form=form)
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    # citylist()
