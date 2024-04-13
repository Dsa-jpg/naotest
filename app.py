from flask import Flask, request, jsonify
from openai import OpenAI
import time
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Initialize OpenAI client
api_key = os.environ.get("OPENAI_API_KEY")
weather_api_key = os.environ.get("WEATHER_API_KEY")
client = OpenAI(api_key=api_key)


@app.route("/")
def home():
    return "<h1>Hello world, Flask on Azure Web App!</h1>"

@app.route('/openAI', methods=['GET'])
def openAI():
    '''
    This method will handle the OpenAI API
    '''

    # Get input text from the query parameters
    input_text = request.args.get('input_text', '')

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

    # Return generated text as JSON response
    response_json = {
        'generated_text': generated_text
    }

    return jsonify(response_json)

if __name__ == "__main__":
    app.run()
