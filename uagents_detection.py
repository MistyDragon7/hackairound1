from uagents import Agent, Context
import json
import requests
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
city = input("Enter City: ")
api_key = os.getenv("API_KEY")
alice = Agent(name = 'alice', seed = 'alics test')
@alice.on_interval(period = 5.0)
async def get_temperature(ctx: Context):
    api_key = os.getenv("API_KEY")
    weather_url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=" + api_key
    data = requests.get(weather_url)
    weather_data = data.json()
    if data.status_code == 200:
        temperature = weather_data['main']['temp']
        temperature = int(temperature)
        #ctx.logger.info(temperature)
        if temperature>300:
            ctx.logger.info("Temperature Too High!!!!")
        elif temperature<250:
            ctx.logger.info("Temperature Too Low!!!!")
    else:
        print(f"Error: {weather_data['message']}")
        return
if __name__ == "__main__":
    alice.run()