#!/usr/bin/python

from spark import app, db, h
from flask import Response, abort, request

@app.route("/Receiver", methods=['POST'])
def MessageReceived():
  from_number = h.sanitizize_num(request.values.get("From"))
  from_message = request.values.get("Body")
  user = db.GetPatientByPhone(h.trim_phone(from_number))

  if not user:
    h.send_message(from_number, h.responses["not_a_patient"])
  else:
    react(user, from_message)

  return Response(response={}, status=200, mimetype="text/xml")

def react(user, message):
  conversation = h.converse(user, message)

  # TODO Once bot is trained, increase value
  #   of confidence check
  if conversation['confidence'] < 0.05:
    return h.send_message(user['phone'], h.responses["cannot_understand"])

  if conversation['type'] == 'stop':
    return

  if conversation['type'] == 'msg':
    h.send_message(user['phone'], conversation['msg'])
  elif conversation['type'] == 'action':
    # perform all actions
  elif conversation['type'] == 'merge':
    # merge contexts

  # Succesively call react until the our
  #   conversation type is 'stop'
  react(user, None)
