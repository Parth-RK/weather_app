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
        user_zipcode = request.form.get("zipcode")
        user_city = request.form.get("city")
        
        # Check if API key is available
        api_key = os.getenv("API_KEY")
        if not api_key:
            return "API key not found. Please set API_KEY in your environment variables."

        # Send request to OpenWeather API
        try:
            # openweather = requests.get(
            #     f"https://api.openweathermap.org/data/2.5/weather?zip={user_zipcode},{user_city}&appid={api_key}&units=imperial"
            # )
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = f"{base_url}q={user_city}&appid={api_key}&units=metric"
            openweather = requests.get(complete_url)
            # Check if the request was successful
            if openweather.status_code == 200:
                weather_data = openweather.json()
                return render_template('index.html', weather=weather_data)
            else:
                # Display error message if request fails
                return f"Error: Unable to fetch data from OpenWeather API. Status code: {openweather.status_code}"
        except requests.RequestException as e:
            # Catch and display request errors
            return f"An error occurred: {e}"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
