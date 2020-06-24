Create a .env file with variables: FLASK_ENV, BOT_TOKEN, API_KEY(optional), API_SECRET(optional).

Create a virtual environment using `virtualenv` and then download packages in `requirements.txt`

Remove any existing webhooks, then set new webhook with hosted url (ex: https://ngrok.io)

Run `Flask run` to run `app.py`


**Telegram webhook methods:**

1. https://api.telegram.org/bot<BOT_TOKEN>/deleteWebhook
2. https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<hosted_url>

