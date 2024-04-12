from flask import Flask, request, jsonify
from openai import OpenAI
import time
from datetime import datetime
import requests

app = Flask(__name__)

# Initialize OpenAI client
api_key = "YOUR_OPENAI_API_KEY"
weather_api_key = "YOUR_WEATHER_API_KEY"
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return "<h1>Hello world, Flask on Azure Web App!</h1>"

@app.route('/openAI', methods=['POST'])
def openAI():
    '''
    This method will handle the OpenAI API
    '''

    # Start measuring processing time
    start_processing_time = time.time()

    # Get input text from the request
    input_text = request.json.get('input_text', '')

    # Get current datetime for the robot's message
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get current weather for Ceske Budejovice from OpenWeatherMap API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q=Ceske%20Budejovice&appid={weather_api_key}"
    response = requests.get(weather_url)
    weather_data = response.json()
    
    # Get weather description
    current_weather = weather_data["weather"][0]["description"]

    # Use OpenAI API to generate text
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106",
                                              messages=[
                                                  {
                                                      "role": "system",
                                                      "content": f"Jsi robot NAO. Je ti 14 let. A žiješ v Českých Budějovicích. Aktuální datum a čas: {current_datetime}. Aktuální počasí v Českých Budějovicích: {current_weather}. A nezmiňuj se o tom, že se jedná o požadavek HTTP POST, jen odpověz na otázku."
                                                  },
                                                  {
                                                      "role": "user",
                                                      "content": input_text,
                                                  }
                                              ])

    # Get generated text from OpenAI API response
    generated_text = response.choices[0].message.content

    # End processing time measurement
    end_processing_time = time.time()
    processing_time = end_processing_time - start_processing_time

    # Return generated text as JSON response
    response_json = {
        'generated_text': generated_text,
        'processing_time': processing_time
    }

    return jsonify(response_json)
