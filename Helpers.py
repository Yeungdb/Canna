#!/usr/bin/python

import os
import ConfigParser

from twilio.rest import Client

current_path = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(current_path, '.env'))

twilio_number = config.get('TWILIO', 'number')
twilio_client = Client(config.get('TWILIO', 'sid'), config.get('TWILIO', 'auth'))

def send_message(number, message):
  return twilio_client.messages.create(
      to=number, 
      from_=twilio_number,
      body=message)