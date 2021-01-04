import requests
import os

web_url = os.environ["web_url"]


def send_error_log(message):
	requests.post(web_url,{"content": message})