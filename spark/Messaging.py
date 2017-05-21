#!/usr/bin/python

from spark import app, db, h
from flask import Response, abort, request
from wit import Wit

wit_token = h.config.get('WIT', 'token')
wit = Wit(access_token=wit_token)

# Load Interactions
from spark.interactions          import Interaction, AcceptedInteractions, responses
from spark.interactions.Orders   import Enquiries
from spark.interactions.Help     import Dispensary, Bot
from spark.interactions.Products import Lookup
from spark.interactions.Goodies  import Goodies

interactions = {}
interactionModules = [Enquiries, Dispensary, Bot, Lookup, Goodies]

for interaction in interactionModules:
  interactions[interaction.identifier] = interaction()

@app.route("/Receiver", methods=['POST'])
def MessageReceived():
  from_number = h.sanitizize_num(request.values.get("From"))
  from_message = request.values.get("Body")
  user = db.GetPatientByPhone(h.trim_phone(from_number))

  if not user:
    h.send_message(from_number, responses["system"]["not_a_patient"])
  else:
    Interaction.user = user
    actionable = interact(from_message)

    if not actionable:
      h.send_message(from_number, responses["system"]["cannot_understand"])

  return Response(response={}, status=200, mimetype="text/xml")

def interact(message):
  response = wit.message(message)
  entities = Interaction.confidentEntities(response['entities'])

  actionable = False

  for key, value in entities.iteritems():
    if key in AcceptedInteractions:
      actionable = True
      last_match = Interaction.lastInteractionMatch(key, value)
      action_result = AcceptedInteractions[key]['action']()

      if not last_match == False:
        Interaction.updateExisting(last_match['id'], action_result)
      else:
        Interaction.createNew(action_result)

      break

  return actionable
