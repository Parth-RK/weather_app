from flask import Flask, request, render_template
import os, requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        user_zipcode = request.form.get("zip")
        user_country_code = request.form.get("country_code")
        
        # Check if API key is available
        api_key = os.getenv("API_KEY")
        if not api_key:
            return "API key not found. Please set API_KEY in your environment variables."

        # Send request to OpenWeather API
        openweather = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?zip={user_zipcode},{user_country_code}&appid={api_key}&units=imperial"
        )
        
        # Check if the request was successful
        if openweather.status_code == 200:
            return render_template('weather.html', weather=openweather.json())
        else:
            return f"Error: Unable to fetch data from OpenWeather API. Status code: {openweather.status_code}"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
