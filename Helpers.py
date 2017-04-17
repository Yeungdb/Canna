#!/usr/bin/python

import os
import ConfigParser
from urlparse import urlparse, urljoin
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

def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc
