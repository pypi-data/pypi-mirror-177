from flask import Flask
from flask import request
from flask import Response
import requests

app = Flask(__name__)
from colorama import init
init()
from colorama import Fore, Back, Style
import sys
import os
import signal

def button(bot=None,chat_id=None,text=None):
            url = f'https://api.telegram.org/bot{bot}/sendMessage'
            payload = {
                'chat_id': chat_id,
                'text': text,
                "reply_markup": {"inline_keyboard": [[{"text":"Visit Unofficed","callback_data":"1"}]]}
                }
   
            r = requests.post(url,json=payload)
            return r

def buttons(bot,id):
            url = f'https://api.telegram.org/bot{bot}/answerCallbackQuery'
            payload = {
                'text': "test",
                'callback_query_id': "1",
                }
   
            r = requests.post(url,json=payload)
            return r