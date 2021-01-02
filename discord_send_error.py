import requests

web_url = 'https://discord.com/api/webhooks/794963895663329280/qyv3HT-Jf47znqXX5I0J7ZdENNGVR3jTPZcoHRp1PIg8WD9Iq_Y-w3NFGXyXYTwieosK'

def send_error_log(message):
	requests.post(web_url,{"content": message})