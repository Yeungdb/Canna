#!/usr/bin/python

from spark import app, db, h
from flask import Response, abort, request
from wit import Wit

# Load Interactions
from spark.interactions.Orders   import Enquiries
from spark.interactions.Help     import Dispensary, Bot
from spark.interactions.Products import Lookup
from spark.interactions.Goodies  import Goodies

wit_token = h.config.get('WIT', 'token')
wit = Wit(access_token=wit_token)

@app.route("/Receiver", methods=['POST'])
def MessageReceived():
  from_number = h.sanitizize_num(request.values.get("From"))
  from_message = request.values.get("Body")
  user = db.GetPatientByPhone(h.trim_phone(from_number))

  if not user:
    h.send_message(from_number, h.responses["not_a_patient"])
  else:
    interact(from_message)

  return Response(response={}, status=200, mimetype="text/xml")

def interact(message):
  print(wit.message(message))
