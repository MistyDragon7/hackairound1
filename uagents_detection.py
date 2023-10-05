from uagents import Agent, Context
import tkinter as tk
import json
from twilio.rest import Client as twilio_client
import requests
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

#   Taking City to be observed as Input

city = input("Enter City: ")

#   Importing Environment Variables

api_key = os.getenv("API_KEY")
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
delivery_phone_number = input("Enter phone number to send alerts to: ")

#    Defining the alert message:

message_client = twilio_client(twilio_account_sid, twilio_auth_token)

upper_limit = int(input("Enter upper limit temperature in Kelvin: "))
lower_limit = int(input("Enter lower limit temperature in kelvin: "))

#   Defining the uAgent:

temp_bot = Agent(name = 'temp_bot', seed = 'main_bot')

@temp_bot.on_interval(period = 300.0)

async def get_temperature(ctx: Context):
    api_key = os.getenv("API_KEY")
    weather_url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=" + api_key
    data = requests.get(weather_url)
    weather_data = data.json()

    if data.status_code == 200:
        temperature = weather_data['main']['temp']
        temperature = int(temperature)
        ctx.logger.info(temperature)

        if temperature>upper_limit:
            ctx.logger.info("Temperature Too High!!!!")

            message = message_client.messages.create(
                from_= twilio_phone_number,
                body = "The upper threshold of temperature has been surpassed!!!!",
                to = delivery_phone_number
                )
            return

        elif temperature<lower_limit:
            ctx.logger.info("Temperature Too Low!!!!")

            message = message_client.messages.create(
                from_= twilio_phone_number,
                body = "The upper threshold of temperature has been surpassed!!!!",
                to = delivery_phone_number
                )
            return

    else:
        print(f"Error: {weather_data['message']}")
        return

if __name__ == "__main__":
    temp_bot.run()
