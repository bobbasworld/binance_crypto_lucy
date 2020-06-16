from tokens import bot_token
import requests
import json

from flask import Flask, request, Response

import os
import sys

import telebot

telegram_api_url = f"https://api.telegram.org/bot{bot_token}/getMe"
binance_api_url = "https://api.binance.com"

app = Flask(__name__)

# initialize telgram bot
bot = telebot.TeleBot(token=bot_token)

# save response data to json file
def write_json(data, filename="response.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# load trade pair symbols from binance
def load_symbols():
    exch_data = requests.get(binance_api_url + "/api/v1/exchangeInfo").json()
    symbols_list = exch_data["symbols"]
    symbols = [s["symbol"] for s in symbols_list]
    return symbols


# Parse the user’s message
def parse_message(message):
    chat_id = message["message"]["chat"]["id"]
    txt = message["message"]["text"]

    symbols = load_symbols()
    input_pair = txt.upper()

    # check if valid input pair
    if input_pair not in symbols:
        return chat_id, None
    else:
        return chat_id, input_pair


# get current price of symbol
def get_current_price(symbol):
    params = {"symbol": symbol.upper()}

    res = requests.get(binance_api_url +
                       "/api/v3/ticker/price", params=params).json()
    price = res["price"]
    print(price)
    return price


# get larget recent trade info
def largest_recent_trade(symbol):
    payload = {"symbol": symbol.upper()}

    recent_trades = requests.get(
        binance_api_url + "/api/v3/trades", params=payload).json()

    resp_list = list()

    for trade in recent_trades:
        price = trade["price"]
        price = float(price)
        quantity = trade["qty"]
        quantity = float(quantity)

        if quantity > 10.0:
            resp = {"Price": price, "Quantity": quantity}
            resp_list.append(resp)

    print(resp_list)
    return resp_list


def send_message(chat_id, text="blah blah blah"):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    r = requests.post(url, json=payload)
    return r



# flask route/webhook
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         msg = request.get_json()
#         chat_id, symbol = parse_message(msg)
#         txt = msg["message"]["text"].lower()
#         # chat_id = msg["message"]["chat"]["id"]

#         if symbol is None:
#             resp = "Please enter a valid trade pair! Ex: ETHBTC"
#             send_message(chat_id, resp)
#             return Response("OK", status=200)

#         price = get_current_price(symbol)
#         send_message(chat_id, f"Price: {price}")

#         # check for end command to stop program

#         # return price and quantity if above 10BTC
#         resp_list = largest_recent_trade(symbol)
#         resp = f"Trades over 10 BTC: {resp_list}"
#         send_message(chat_id, resp)
#         # for i in resp_list:
#         #     p = i["Price"]
#         #     q = i["Quantity"]

#         #     resp = f"Price: {p}\nQuantity: {q}"
#         #     send_message(chat_id, resp)
        

#             # write_json(msg, "telegram_request.json")

#         return Response("OK", status=200)
#     else:
#         return "<h1>Coin Whispers Bot!</h1>"


@bot.message_handler(commands=["track"])
def track(message):
    bot.reply_to(message, "Please enter a trade pair to track: (ex: BTCUSDT)")
    txt = message.text.upper()
    # send_message(message, "Please enter a trade pair to track: (ex: BTCUSDT)")

    symbols = load_symbols()

    if txt in symbols:
        # get larget_recent_trade
        values = largest_recent_trade(txt)
        print(values)
        return Response("OK", status=200)
    else:
        bot.reply_to(message, "Please enter a trade pair to track: (ex: BTCUSDT)")
        return Response("OK", status=200)


def main():
    largest_recent_trade("btcusdt")

    # https://api.telegram.org/bot1097324524:AAGyTMdsD9CvOBfOuM8_CHIHlq49R6puHFU/sendMessage?chat_id=988289234&text=Hello User
    # https://api.telegram.org/bot1097324524:AAGyTMdsD9CvOBfOuM8_CHIHlq49R6puHFU/setWebhook?url=https://93dbe5d24981.ngrok.io


if __name__ == "__main__":
    # main()
    app.run(debug=True)
