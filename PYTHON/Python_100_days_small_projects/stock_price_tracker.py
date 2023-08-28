import requests
import os
from twilio.rest import Client

STOCK = "SE"
COMPANY_NAME = "Sea Limited"
DOWN_EMOJI = "\U0001F53B"
UP_EMOJI = "\U0001F53A"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
parameters = {
    "news":{
    "api_key":"479fa77fccf54fda8721a2c82eb36c01",
    "topic":COMPANY_NAME
    },
    "stocks":{
        "api_key":"1ATTURPG7WQ19X5O",
        "topic": STOCK
    }
}
account_sid = "AC596522e694893cf92845dff5d6c9da0e"
auth_token = "88d91f1f5074dbd02cda2eea9af14989"
client = Client(account_sid, auth_token)

request_url_stock = STOCK_ENDPOINT+"?function=TIME_SERIES_DAILY&symbol="+parameters["stocks"]["topic"]+"&outputsize=compact&apikey="+parameters["stocks"]["api_key"]
response_stock = requests.get(request_url_stock).json()["Time Series (Daily)"]
dates_to_consider= [value for value in response_stock.keys()][:2]

price_change = float(response_stock[dates_to_consider[0]]['4. close']) - float(response_stock[dates_to_consider[1]]['4. close'])

if abs(price_change) > 0.05 * float(response_stock[dates_to_consider[1]]['4. close']):
    request_url_news = NEWS_ENDPOINT + "?q=" + parameters["news"]["topic"] + "&apiKey=" + parameters["news"]["api_key"]
    response_news = requests.get(request_url_news).json()["articles"][:3]
    message_body = ""
    for item in response_news:
        message_body += f"""{STOCK} : {UP_EMOJI if price_change > 0 else DOWN_EMOJI} {(abs(price_change/float(response_stock[dates_to_consider[1]]['4. close']))):.0%}  
        Headline : {item['title']}
        Brief: {item['description']}
"""
    message = client.messages \
        .create(
        body=message_body,
        from_='+18645276331',
        to='+48511111369'
    )

