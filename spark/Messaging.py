#!/usr/bin/python

from spark import app, h
from flask import Response, abort, request
import json

@app.route("/Receiver", methods=['POST'])
def MessageReceived():
  from_number = h.sanitizize_num(request.values.get("From"), False)
  from_message = request.values.get("Body")

  print ("New message from " + from_number + ": " + from_message)
  return Response(response={}, status=200, mimetype="application/json")
