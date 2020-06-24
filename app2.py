import os

from flask import Flask, request

import telebot
from tokens import bot_token
from helpers import *



TOKEN = bot_token
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, welcome to Crypto Lucy! Type '/help' for command list")


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "🤖 /start - display the keyboard\n"
									  "💎 /track - current cryptocurrency\n"
                                      "💲/price - current crypto price\n"
                                      )

@bot.message_handler(commands=['price'])
def price(message):
    sent = bot.send_message(message.chat.id, "Please enter a trade pair: ")
    bot.register_next_step_handler(sent, send_price)


def send_price(message):
    try: 
        symbol = parse_message(message)

        if symbol is not None:
            price = get_current_price(symbol)
            bot.reply_to(message, f"Price: {price}")
        else:
            bot.reply_to(message, "Enter a valid trade pair!")
            
    except Exception as e:
        bot.reply_to(message, "Something went wrong!")
        print("Error: ", e)


@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://9570854bd96e.ngrok.io/' + TOKEN)
    return "!", 200



if __name__ == "__main__":
    app.run(debug=True)