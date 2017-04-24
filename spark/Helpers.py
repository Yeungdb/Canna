#!/usr/bin/python

import os
import json
import ConfigParser
from urlparse import urlparse, urljoin
from twilio.rest import Client

current_path = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(current_path, '../', '.env'))

twilio_number = config.get('TWILIO', 'number')
twilio_client = Client(config.get('TWILIO', 'sid'), config.get('TWILIO', 'auth'))

env = config.get('APP', 'env')

def send_message(number, message):
  return twilio_client.messages.create(
    to=number, 
    from_=twilio_number,
    body=message)

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def ngrok_address():
  os.system("curl http://localhost:4040/api/tunnels > tunnels.json")

  with open('tunnels.json') as data_file:    
    address = json.load(data_file)['tunnels'][1]['public_url']

  message = "DEVELOPMENT MODE \n" + \
            "ngrok address: " + address

  print(message)
