# from flask import Flask, request, render_template
# import os, requests
# from dotenv import load_dotenv
# import yfinance as yf

# load_dotenv()
# app = Flask(__name__)

# @app.route('/', methods=["GET", "POST"])
# def index():
#     if request.method == 'GET':
#         return render_template("index.html")
#     elif request.method == 'POST':
#         user_zipcode = request.form.get("zipcode")
#         user_city = request.form.get("city")
        
#         # Check if API key is available
#         api_key = os.getenv("API_KEY")
#         api_key_news = os.getenv("NEWS_API_KEY")

#         if not api_key:
#             return "API key not found. Please set API_KEY in your environment variables."

#         try:
#             # Fetch weather data
#             base_url = "http://api.openweathermap.org/data/2.5/weather?"
#             complete_url = f"{base_url}q={user_city}&appid={api_key}&units=metric"
#             openweather = requests.get(complete_url)

#             # Fetch stock data
#             nifty = yf.Ticker("^NSEI")
#             sensex = yf.Ticker("^BSESN")

#             nifty_data = nifty.history(period="5d")  # Fetch data for the last two days
#             sensex_data = sensex.history(period="5d")
            
#             print(nifty_data)
#             print(sensex_data)
            
#             # Calculate latest close prices and differences
#             if not nifty_data.empty and len(nifty_data) >= 5:
#                 nifty_close = nifty_data['Close'].iloc[-1]
#                 nifty_prev_close = nifty_data['Close'].iloc[-2]
#                 nifty_diff = nifty_close - nifty_prev_close
#             else:
#                 nifty_close = nifty_diff = None

#             if not sensex_data.empty and len(sensex_data) >= 5:
#                 sensex_close = sensex_data['Close'].iloc[-1]
#                 sensex_prev_close = sensex_data['Close'].iloc[-2]
#                 sensex_diff = sensex_close - sensex_prev_close
#             else:
#                 sensex_close = sensex_diff = None

            
#             # Fetch headlines from NewsData.io
#             news_url = f"https://newsdata.io/api/1/news?apikey={api_key_news}&country=in&language=en&category=business"
#             news_response = requests.get(news_url)
#             print("NewsData.io API response:", news_response.json())  # Debugging line

#             # Extract articles if response is valid
#             if news_response.status_code == 200:
#                 headlines = news_response.json().get('results', [])
#             else:
#                 headlines = []

#              # Fetch Quote of the Day from ZenQuotes
#             quote_url = "https://zenquotes.io/api/today"
#             quote_response = requests.get(quote_url)
#             if quote_response.status_code == 200:
#                 quote_data = quote_response.json()
#                 quote_text = quote_data[0]['q']
#                 quote_author = quote_data[0]['a']
#             else:
#                 quote_text, quote_author = "Stay positive and keep pushing forward!", "Unknown"

#             # Render only if data is available
#             if openweather.status_code == 200:
#                 weather_data = openweather.json()
#                 return render_template(
#                     'index.html', 
#                     weather=weather_data, 
#                     nifty=nifty_close, 
#                     nifty_diff=nifty_diff, 
#                     sensex=sensex_close, 
#                     sensex_diff=sensex_diff,
#                     headlines=headlines,
#                      quote_text=quote_text, 
#                     quote_author=quote_author
#                 )
#             else:
#                 # Display error message if request fails
#                 return f"Error: Unable to fetch data. Weather status: {openweather.status_code}"
                
#         except requests.RequestException as e:
#             # Catch and display request errors
#             return f"An error occurred: {e}"

# # Run the application
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template
import os, requests
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    api_key_news = os.getenv("NEWS_API_KEY")  # NewsData.io API key
    api_key_weather = os.getenv("API_KEY")     # OpenWeatherMap API key
    api_key_cricket = os.getenv("CRICKET_API_KEY") # CricAPI key
    
    # Fetch stock, news, and quote data on both GET and POST requests
    # Fetch stock data
    nifty = yf.Ticker("^NSEI")
    sensex = yf.Ticker("^BSESN")
    nifty_data = nifty.history(period="5d")
    sensex_data = sensex.history(period="5d")

    nifty_close = nifty_data['Close'].iloc[-1] if not nifty_data.empty else None
    sensex_close = sensex_data['Close'].iloc[-1] if not sensex_data.empty else None
    nifty_diff = nifty_data['Close'].iloc[-1] - nifty_data['Close'].iloc[-2] if len(nifty_data) > 1 else None
    sensex_diff = sensex_data['Close'].iloc[-1] - sensex_data['Close'].iloc[-2] if len(sensex_data) > 1 else None

    # Fetch headlines from NewsData.io
    news_url = f"https://newsdata.io/api/1/news?apikey={api_key_news}&country=in&language=en&category=business"
    news_response = requests.get(news_url)
    headlines = news_response.json().get('results', []) if news_response.status_code == 200 else []

    # Fetch Quote of the Day from ZenQuotes
    quote_url = "https://zenquotes.io/api/today"
    quote_response = requests.get(quote_url)
    if quote_response.status_code == 200:
        quote_data = quote_response.json()
        quote_text = quote_data[0]['q']
        quote_author = quote_data[0]['a']
    else:
        quote_text, quote_author = "Stay positive and keep pushing forward!", "Unknown"

   

    
    
    # Initialize weather data as None
    weather_data = []

    # Fetch weather data only if city is provided (POST request)
    if request.method == 'POST':
        user_city = request.form.get("city")
        if user_city and api_key_weather:
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={api_key_weather}&units=metric"
            openweather = requests.get(weather_url)
            weather_data = openweather.json() if openweather.status_code == 200 else None

    return render_template(
        'index.html',
        weather=weather_data,
        nifty=nifty_close,
        nifty_diff=nifty_diff,
        sensex=sensex_close,
        sensex_diff=sensex_diff,
        headlines=headlines,
        quote_text=quote_text,
        quote_author=quote_author,
    )

if __name__ == '__main__':
    app.run(debug=True)
