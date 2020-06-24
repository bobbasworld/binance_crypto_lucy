import os

from dotenv import load_dotenv
load_dotenv()

# telegram 
bot_token= os.environ["BOT_TOKEN"]
# bot_user_name=CoinWhispersBot
# URL=https://coin-whispers-bot.herokuapp.com/

# binance
api_key= os.environ["API_KEY"]
api_secret= os.environ["API_SECRET"]
