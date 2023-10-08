#importing necessary libraries
from uagents import Agent, Context
import json
from twilio.rest import Client as twilio_client
import requests
from dotenv import load_dotenv, find_dotenv
import os
import asyncio
from datetime import datetime
import mysql.connector
from mysql.connector import Error

#Defining MySQL connection
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_db_connection("localhost", "root", "1234", "tempy")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(*query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")
        

#Loading envuronment variables file
load_dotenv(find_dotenv())

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

tempy = Agent(name = 'tempy', seed = 'main_bot')

@tempy.on_interval(period = 300.0)

async def get_temperature(ctx: Context):
    api_key = os.getenv("API_KEY")
    weather_url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=" + api_key
    data = requests.get(weather_url)
    weather_data = data.json()
    now = datetime.now()
    if data.status_code == 200:
        temperature = weather_data['main']['temp']
        temperature = int(temperature)
        ctx.logger.info(temperature)
        sql = """INSERT INTO temperature_data(
            Temperature, Location, Datetime)
            VALUES (%s, %s, %s);""", (temperature, city, now)
        execute_query(connection, sql)
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
