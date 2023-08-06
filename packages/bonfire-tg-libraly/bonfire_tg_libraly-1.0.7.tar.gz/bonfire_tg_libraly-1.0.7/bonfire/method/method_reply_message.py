from flask import Flask
from flask import request
from flask import Response
import requests
import os
import signal
app = Flask(__name__)
from colorama import init
init()
from colorama import Fore, Back, Style
import sys

def reply_parse_message(message=None):
   if message == None:
     print(Fore.RED+f"You did not specify a keyword in the 'reply_parse_message' function (line : {sys._getframe(1).f_lineno})"+Style.RESET_ALL)
     print(Fore.RED+f"Ви не вказали ключове слово в функціі 'reply_parse_message'  (лінія :{sys._getframe(1).f_lineno})"+Style.RESET_ALL)
     sig = getattr(signal, "SIGKILL", signal.SIGTERM)
     os.kill(os.getpid(), sig)

   try:
    reply_message_text = message['message']['reply_to_message']['text']
    reply_message_id = message['message']['reply_to_message']['message_id']

    return reply_message_text,reply_message_id
   except :
    pass

def reply_parse_message_text(message=None):
   if message == None:
     print(Fore.RED+f"You did not specify a keyword in the 'reply_parse_message' function (line : {sys._getframe(1).f_lineno})"+Style.RESET_ALL)
     print(Fore.RED+f"Ви не вказали ключове слово в функціі 'reply_parse_message'  (лінія :{sys._getframe(1).f_lineno})"+Style.RESET_ALL)
     sig = getattr(signal, "SIGKILL", signal.SIGTERM)
     os.kill(os.getpid(), sig)

   try:
    reply_message_text = message['message']['reply_to_message']['text']

    return reply_message_text
   except :
    pass