from flask import Flask, jsonify, render_template, request, session
import requests
import datetime
from cs50 import SQL
from flask_session import Session

app = Flask(__name__,static_folder='statics')

db = SQL("sqlite:///weather.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET','POST'])

def weather():
    if request.method == "GET":

        if "name" not in session:
            session["name"] = []

        response = requests.get('http://ip-api.com/json/')
        data_user= response.json()

        if "error" in data_user:
            return render_template('weather.html', invalid=True)

        city_user = data_user['city']
        api_key = 'e49f4812e5e84d5b93c10626241612'
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_user}&days=7&aqi=yes&alerts=yes'

        response = requests.get(url).json()
        name = response['location'].get('name')
        region = response['location'].get('region')
        country = response['location'].get('country')
        temp_c = response['current'].get('temp_c')
        temp_l_0= response['forecast']['forecastday'][0]['day'].get('mintemp_c')
        temp_h_0= response['forecast']['forecastday'][0]['day'].get('maxtemp_c')
        description = response['current']['condition'].get('text')
        wind = response['current'].get('wind_kph')
        humidity = response['current'].get('humidity')
        icon_c = response['current']['condition'].get('icon')
        last_updated = response['current'].get('last_updated')
        date = response['forecast']['forecastday'][0].get('date')
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        day0 = date_obj.strftime("%a")
        daily_chance_of_rain = response['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain')

        # Weather description rename for CSS background(no blank in string)
        description_p = description.replace(" ", "")

        city_again = db.execute("SELECT DISTINCT city FROM (SELECT city FROM city_search WHERE city IN (?) ORDER BY id DESC) LIMIT 5", session["name"])

        # Forcast Weather
        forecast_data = []
        for day in response['forecast']['forecastday'][1:6]:
                date = day['date']
                temp = day['day']['avgtemp_c']
                temp_h=day['day']['maxtemp_c']
                temp_l=day['day']['mintemp_c']
                icon = day['day']['condition']['icon']
                date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
                day = date_obj.strftime("%a")
                day_of_month = date_obj.strftime("%d")
                forecast_data.append({'day': day, 'temp': temp, 'icon': icon, 'temp_h': temp_h, 'temp_l': temp_l, 'day_of_month':day_of_month})

        # Current Weather of searched cites
        weather_data = []
        for city in city_again:
                        response_s= requests.get(f"http://api.weatherapi.com/v1/forecast.json?key=e49f4812e5e84d5b93c10626241612&q={city['city']}&days=1").json()
                        if 'current' in response_s:
                            weather_data.append({
                                "city": city['city'],
                                "temp": response_s['current']['temp_c'],
                                "icon": response_s['current']['condition']['icon']
                            })



        return render_template('weather.html',
            name=name,
            region=region,
            country=country,
            temp_c=temp_c,
            temp_h_0=temp_h_0,
            temp_l_0=temp_l_0,
            description=description,
            wind=wind, humidity=humidity,
            daily_chance_of_rain=daily_chance_of_rain,
            icon_c=icon_c,
            last_updated=last_updated,
            day0=day0,
            forecast_data=forecast_data,
            weather_data=weather_data,
            description_p = description_p)


    if request.method == "POST":

        city = request.form.get('city')
        api_key = 'e49f4812e5e84d5b93c10626241612'
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&aqi=yes&alerts=yes'

        response = requests.get(url).json()

        if "error" in response:
            return render_template('index.html', invalid=True)
        else:
            # Current Weather
            name = response['location'].get('name')

            db.execute("INSERT INTO city_search (city) VALUES(?)",name)
            session["name"].append(name)
            city_again = db.execute("SELECT DISTINCT city FROM (SELECT city FROM city_search WHERE city IN (?) ORDER BY id DESC) LIMIT 5", session["name"])


            region = response['location'].get('region')
            country = response['location'].get('country')
            temp_c = response['current'].get('temp_c')
            temp_l_0= response['forecast']['forecastday'][0]['day'].get('mintemp_c')
            temp_h_0= response['forecast']['forecastday'][0]['day'].get('maxtemp_c')
            description = response['current']['condition'].get('text')
            wind = response['current'].get('wind_kph')
            humidity = response['current'].get('humidity')
            icon_c = response['current']['condition'].get('icon')
            last_updated = response['current'].get('last_updated')
            date = response['forecast']['forecastday'][0].get('date')
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
            day0 = date_obj.strftime("%a")

            # Current Weather of searched cites
            weather_data = []
            for city in city_again:
                    response_s= requests.get(f"http://api.weatherapi.com/v1/forecast.json?key=e49f4812e5e84d5b93c10626241612&q={city['city']}&days=1").json()
                    if 'current' in response_s:
                        weather_data.append({
                            "city": city['city'],
                            "temp": response_s['current']['temp_c'],
                            "icon": response_s['current']['condition']['icon']
                        })

            # Daily Chance of Rain (Today)
            daily_chance_of_rain = response['forecast']['forecastday'][0]['day'].get('daily_chance_of_rain')

            description_p = description.replace(" ", "")

            # Forcast Weather
            forecast_data = []
            for day in response['forecast']['forecastday'][1:6]:
                date = day['date']
                temp = day['day']['avgtemp_c']
                temp_h=day['day']['maxtemp_c']
                temp_l=day['day']['mintemp_c']
                icon = day['day']['condition']['icon']
                date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
                day = date_obj.strftime("%a")
                day_of_month = date_obj.strftime("%d")
                forecast_data.append({'day': day, 'temp': temp, 'icon': icon, 'temp_h': temp_h, 'temp_l': temp_l, 'day_of_month':day_of_month})

            return render_template('weather.html',
            city_again=city_again,
            weather_data=weather_data,
            name=name,
            region=region,
            country=country,
            temp_c=temp_c,
            temp_h_0=temp_h_0,
            temp_l_0=temp_l_0,
            description=description,
            wind=wind, humidity=humidity,
            daily_chance_of_rain=daily_chance_of_rain,
            icon_c=icon_c,
            last_updated=last_updated,
            day0=day0,
            forecast_data=forecast_data,
            description_p=description_p)



if __name__ == '__main__':
    app.run(debug=True)
