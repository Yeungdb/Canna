#!/usr/bin/python

import os
import json
import webbrowser
import re
import ConfigParser
from urlparse import urlparse, urljoin
from twilio.rest import Client

current_path = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(current_path, '../', '.env'))

twilio_number = config.get('TWILIO', 'number')
twilio_client = Client(config.get('TWILIO', 'sid'), config.get('TWILIO', 'auth'))

env = config.get('APP', 'env')

with open(os.path.join(current_path, '../', 'resources', 'responses.json')) as data_file:
  responses = json.load(data_file)

# Dev Helpers

def start_ngrok():
  os.system("curl http://localhost:4040/api/tunnels > tunnels.json")

  with open('tunnels.json') as data_file:
    address = json.load(data_file)['tunnels'][1]['public_url']

  message = "DEVELOPMENT MODE \n" + \
            "ngrok address: " + address

  webbrowser.open(address)
  print(message)

# Generic Helpers

def send_message(number, messages):
  def _create_message(message):
    twilio_client.messages.create(
      to=number,
      from_=twilio_number,
      body=message)

  if isinstance(messages, list):
    for message in messages:
      _create_message(message)
  else:
    _create_message(messages)

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# Number Helpers

def sanitizize_num(num, to_int=True):
  sanitized_num = re.sub('[^0-9]', '', num)

  if to_int:
    return int(float(sanitized_num))
  else:
    return sanitized_num

def trim_phone(num):
  if len(num) == 11 and num[0] == "1":
    return num[1:]
  return num

