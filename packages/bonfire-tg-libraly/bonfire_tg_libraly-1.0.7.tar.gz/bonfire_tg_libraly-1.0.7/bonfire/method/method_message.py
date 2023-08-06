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

def parse_message(message=None):
 try:
    if message==None:
      print(Fore.RED+f"You did not specify a keyword in the 'parse_message' function (line : {sys._getframe(1).f_lineno})"+Style.RESET_ALL)  
      print(Fore.RED+f"Ви не вказали ключове слово в функціі 'parse_message'  (лінія :{sys._getframe(1).f_lineno})"+Style.RESET_ALL)
      sig = getattr(signal, "SIGKILL", signal.SIGTERM)
      os.kill(os.getpid(), sig)
      

    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    message_id=message['message']['message_id']
    message_author_username=message['message']['from']['username']
    message_author_id=message['message']['from']['id']
    message_author_is_bot=message['message']['from']['is_bot']
    message_author_first_name=message['message']['from']['first_name']
    message_author_language_code=message['message']['from']['language_code']
    message_date=message['message']['date']

    return chat_id,text,message_id,message_author_username,message_author_id,message_author_is_bot,message_author_first_name,message_author_language_code,message_date



    return chat_id,text
 except :
      pass