from flask import Flask, request, render_template
import os, requests
from dotenv import load_dotenv
import yfinance as yf

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

        try:
            # Fetch weather data
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = f"{base_url}q={user_city}&appid={api_key}&units=metric"
            openweather = requests.get(complete_url)

            # Fetch stock data
            nifty = yf.Ticker("^NSEI")
            sensex = yf.Ticker("^BSESN")

            nifty_data = nifty.history(period="5d")  # Fetch data for the last two days
            sensex_data = sensex.history(period="5d")
            print(nifty_data)
            print(sensex_data)
            # Calculate latest close prices and differences
            if not nifty_data.empty and len(nifty_data) >= 5:
                nifty_close = nifty_data['Close'].iloc[-1]
                nifty_prev_close = nifty_data['Close'].iloc[-2]
                nifty_diff = nifty_close - nifty_prev_close
            else:
                nifty_close = nifty_diff = None

            if not sensex_data.empty and len(sensex_data) >= 5:
                sensex_close = sensex_data['Close'].iloc[-1]
                sensex_prev_close = sensex_data['Close'].iloc[-2]
                sensex_diff = sensex_close - sensex_prev_close
            else:
                sensex_close = sensex_diff = None

            # Render only if data is available
            if openweather.status_code == 200:
                weather_data = openweather.json()
                return render_template(
                    'index.html', 
                    weather=weather_data, 
                    nifty=nifty_close, 
                    nifty_diff=nifty_diff, 
                    sensex=sensex_close, 
                    sensex_diff=sensex_diff
                )
            else:
                # Display error message if request fails
                return f"Error: Unable to fetch data. Weather status: {openweather.status_code}"
                
        except requests.RequestException as e:
            # Catch and display request errors
            return f"An error occurred: {e}"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

