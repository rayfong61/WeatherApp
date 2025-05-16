# Weather App
#### Video Demo:  <https://youtu.be/NNO4vuKKK4U>

Weather App is a simple web-based application that allows users to search for current and forecast weather for any location in the world. It also stores the cities that users have searched for and displays the latest 5 searched cities' current weather on the header.

## Installation:

- Clone the repository.
- Install the required dependencies using pip install -r requirements.txt.
- Set up the database by running the provided SQL script.
- Obtain an API key from WeatherAPI and configure it in your application.
- Run the application using flask run.

## Usage:

- Open the application in your web browser.
- Use the search bar to find the weather for any city or location.
- View the current weather and 5-day forecast.
- Click on previously searched cities to quickly view their current weather.

## Features:

- Search for weather by city/location.
- Real-time weather data including temperature, humidity, wind speed, and weather conditions.
- 5-day weather forecast.
- Dynamic backgrounds that change with the current weather.
- Quick access to recently searched cities.

To implement these features of the app, I looked up some real weather forcaste websites for inspiration. And I choose The Weather Channel as an imitation object for this project. I designed a header including logo, search bar, and searched cites with their current weather conditions, then the main part is a weather-card with current data and 5-day forcast of the weather of the city user just searched for, and also a footer including the link of WeatherAPI.

In the header of the website, I need to create a search bar in the header. The search bar in The Weather Channel is very frendly for users, because it use autotype function to avoid users type incorrectly when searching the city of location. I implemented the search bar by studying some examples on [BootstrapExamples]. Then I use the GoogleAPI for implementing the autotype function by adding some Javascript in HTML of the search bar.

To create a weather-card with the weather data including time, location, current condition such as weather icon, description, temperature, wind, humidity and chance of rain, we must seek for the API that provides the data of the global weather. Therefore, I went to WeatherAPI.com and studied how to fetch the weather data of the cites/location around the world.

One special featrue for me is to let users see different backgrounds with different weather conditions. The way to do this effect in this project is simple. In the HTML , make a CSS class of body and name it the same as the description of the weather. Then change the picture of background in CSS file. One thing to note is that the name of class must be no blank in string. But the weather descriptions are usually icluding blank such as "Light rain","Patchy rain nearby". So I make a variable called description_p that replace the blank with "" in Python.
```sh
description_p = description.replace(" ", "")
```
So in the layout.HTML, We must make a body class like this:
```sh
<body class="{{ description_p }}">
```

And this is how to code the class of the body. Here I make the cloud.jpg as the defalt backgound.
```sh
body {
  background: url('/statics/cloud.jpg') no-repeat center center fixed;
  background-size: cover;
}

.Sunny {
  background: url('/statics/sunny.jpg') no-repeat center center fixed;
  background-size: cover;
}

.Clear {
  background: url('/statics/clear.jpg') no-repeat center center fixed;
  background-size: cover;
}

.Rainy , .Patchyrainnearby, .Lightrain, .Lightrainshower, .Moderaterainattimes{
  background: url('/statics/rain.jpg') no-repeat center center fixed;
  background-size: cover;
}

.HeavySnow , .Patchylightsnow, .Lightsnow{
  background: url('/statics/snow.jpg') no-repeat center center fixed;
  background-size: cover;
}

.Overcast{
  background: url('/statics/overcast.jpg') no-repeat center center fixed;
  background-size: cover;
}
```

To make a quick access to recently searched cities in the header is quite challenging for me. I reviewed some lectures about how to make this fuction with Flask, session and SQLite3. First I created a database called weather.db to store cities that user searched. In the weather.db, there's a table called city_search which provide the id and city each time searced by users.
```sh
project/ $ sqlite3 weather.db
sqlite> .schema
CREATE TABLE city_search(
id INTEGER,
city TEXT NOT NULL,
PRIMARY KEY(id)
);
```
Then we have to create a list by SQL and session to get the laties 5 cities that users searched before:
```sh
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
            city_again = db.execute("SELECT DISTINCT city FROM (SELECT city FROM city_search WHERE city IN (?) ORDER BY id DESC) LIMIT 5", session["name"])

    if request.method == "POST":
        city = request.form.get('city')
        db.execute("INSERT INTO city_search (city) VALUES(?)",name)
        session["name"].append(name)
        city_again = db.execute("SELECT DISTINCT city FROM (SELECT city FROM city_search WHERE city IN (?) ORDER BY id DESC) LIMIT 5", session["name"])
```
And for the HTML part of the searched cites part:
```sh
<div id="searched_cites" class="container " >
     <div id="searched_cites" class="btn-group  d-flex" role="group">
        {% for data in weather_data %}
            <form action="/" method="post" class="d-inline">
              <input type="hidden" name="city" value="{{ data.city }}">
              <button type="submit" class="btn text-white">
              <img src="{{ data.icon }}" alt="Weather Icon">{{ data.temp }}° {{ data.city }}
              </button>
            </form>
        {% endfor %}
     </div>
</div>
```
## Technologies:

- Frontend: HTML/CSS for designing the layout.
- Backend: Flask/Python/Javascript for handling user requests.
- Database: SQLite for storing search history.
- API Integration: WeatherAPI for fetching weather data.

## Contributors:

- JUI-FENG LU

## License:

- No license

## References/Resources:

- CS50 Duck Debugger
- ChatGPT
- Bootstrap
- Stackoverflow
- Python Forum
- W3 Schools
- WeatherAPI
- The Weather Channel
- Pinterest
- Bootstrapexamples

[//]: #

[BootstrapExamples]: <https://bootstrapexamples.com/>
