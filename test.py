import requests

base_url = "https://api.binance.com"

symbol = input("Enter a symbol: ").upper()
params = {"symbol": symbol}

resp = requests.get(base_url + "/api/v3/ticker/price", params=params).json()

print(resp)