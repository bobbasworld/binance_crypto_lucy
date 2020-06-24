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
# def parse_message(message):
#     chat_id = message["message"]["chat"]["id"]
#     txt = message["message"]["text"]

#     symbols = load_symbols()
#     input_pair = txt.upper()

#     # check if valid input pair
#     if input_pair not in symbols:
#         return chat_id, None
#     else:
#         return chat_id, input_pair


# get current price of symbol
def get_current_price(symbol):
    params = {"symbol": symbol.upper()}

    res = requests.get(binance_api_url +
                       "/api/v3/ticker/price", params=params).json()
    price = res["price"]
    # print(price)
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
        quantity = round(float(quantity), 2)
        amount = price * quantity

        if amount > 0.5:
            resp = {"Price": price, "Quantity": quantity}
            resp_list.append(resp)

    # print(resp_list)
    return resp_list


def send_message(chat_id, text="blah blah blah"):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    r = requests.post(url, json=payload)
    return r


# flask route/webhook
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        msg = request.get_json()
        # chat_id, symbol = parse_message(msg)
        symbols = load_symbols()
        txt = msg["message"]["text"].upper()
        chat_id = msg["message"]["chat"]["id"]
        

        if (txt not in symbols) or ("BTC" not in txt):
            resp = "Please enter a valid BTC pair! Ex: ETHBTC"
            send_message(chat_id, resp)
            return Response("OK", status=200)

        price = get_current_price(txt)
        send_message(chat_id, f"💰Current Price in BTC: {price}")

        # Ask for trade pair to track


        # return price and quantity if above 10BTC
        resp_list = largest_recent_trade(txt)
        
        # check if trades above 0.5 BTC found
        if len(resp_list) > 0:
            # resp = f"Trades over 10 BTC: \n{resp_list}"
            # send_message(chat_id, resp)
            trade_list = []
            for i in resp_list:
                p = i["Price"]
                q = i["Quantity"]

                trade_list.append(f"""Price: {p}   Quantity: {q}""" )

            trade_list = str(trade_list)[1:-1]    
            send_message(chat_id, f" ✅ Trades over 0.5 BTC:\n\n{trade_list}")
        else:
            resp = "❌ No trades over 0.5 BTC!"
            send_message(chat_id, resp)
        

            # write_json(msg, "telegram_request.json")

        return Response("OK", status=200)
    else:
        return "<h1>Crypto Lucy!</h1>"


# @bot.message_handler(commands=["track"])
# def track(message):
#     bot.reply_to(message, "Please enter a trade pair to track: (ex: BTCUSDT)")
#     txt = message.text.upper()
#     # send_message(message, "Please enter a trade pair to track: (ex: BTCUSDT)")

#     symbols = load_symbols()

#     if txt in symbols:
#         # get larget_recent_trade
#         values = largest_recent_trade(txt)
#         print(values)
#         return Response("OK", status=200)
#     else:
#         bot.reply_to(message, "Please enter a trade pair to track: (ex: BTCUSDT)")
#         return Response("OK", status=200)


def main():
    return
    # largest_recent_trade("ethbtc")

    # msg = input("Enter a trade pair: ").upper()
    # symbols = load_symbols()

    # while msg not in symbols:
    #     print("Invalid pair!")
    #     msg = input("Enter a trade pair: ").upper()
    # else:
    #     price = get_current_price(msg)
    #     print("Price: ", price)
       
    # # Get recent trades
    # msg1 = input("which pair do you want to track?: ").upper()
    # while msg1 not in symbols:
    #     print("Not a valid pair (ex: BTCUSDT)")
    #     msg1 = input("which pair do you want to track?: ").upper()
    # else:
    #     trades_list = largest_recent_trade(msg1)
    #     for item in trades_list:
    #         print(item)

    # https://api.telegram.org/bot1097324524:AAGyTMdsD9CvOBfOuM8_CHIHlq49R6puHFU/sendMessage?chat_id=988289234&text=Hello User
    # https://api.telegram.org/bot1097324524:AAGyTMdsD9CvOBfOuM8_CHIHlq49R6puHFU/setWebhook?url=https://5e46c6b90744.ngrok.io


if __name__ == "__main__":
    # main()
    app.run(debug=True)
