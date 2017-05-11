#!/usr/bin/python

from spark import app, db, h
from flask import Response, abort, request
import json

@app.route("/Receiver", methods=['POST'])
def MessageReceived():
  from_number = h.sanitizize_num(request.values.get("From"), False)
  from_message = request.values.get("Body")
  user = db.GetPatientByPhone(h.trim_phone(from_number))

  # User will be False or a Dictionary

  # Return XML response
  return Response(response={}, status=200, mimetype="text/xml")
