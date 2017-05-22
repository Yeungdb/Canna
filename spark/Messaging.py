#!/usr/bin/python

from spark import app, db, h
from flask import Response, abort, request
from wit   import Wit

wit_token = h.config.get('WIT', 'token')
wit = Wit(access_token=wit_token)

# Load Interactions
from spark.interactions          import Interaction, AcceptedInteractions, responses
from spark.interactions.Users    import Onboarding
from spark.interactions.Orders   import Enquiries
from spark.interactions.Help     import Dispensary, Bot
from spark.interactions.Products import Lookup
from spark.interactions.Goodies  import Goodies

interactions = {}
interactionModules = [Onboarding, Enquiries, Dispensary, Bot, Lookup, Goodies]

for interaction in interactionModules:
  interactions[interaction.identifier] = interaction()

# Route to receive messages
@app.route('/Receiver', methods=['POST'])
def MessageReceived():
  from_number = h.sanitizize_num(request.values.get('From'))
  from_message = request.values.get('Body')
  user = db.GetPatientByPhone(h.trim_phone(from_number))

  if not user:
    h.send_message(from_number, responses['system']['not_a_patient'])
  else:
    Interaction.user = user
    Interaction.dispensary = db.GetDispensaryFromPatient(user['phone'])
    actionable = interact(from_message)

    if not actionable:
      h.send_message(from_number, responses['system']['cannot_understand'])

  return Response(response={}, status=200, mimetype='text/xml')

# Parse incoming message and perform applicable interactions
def interact(message):
  response = wit.message(message)
  entities = Interaction.confidentEntities(response['entities'])

  actionable = False

  for entity, value in entities.iteritems():
    last_interaction = Interaction.lastInteractionMatch(entity)
    if last_interaction:
      actionable = True
      next_interaction = last_interaction['state']['values'][value[0]]
      Interaction.last_interaction = last_interaction
      AcceptedInteractions[next_interaction]()
      break

  if not actionable:
    for entity, value in entities.iteritems():
      if entity in AcceptedInteractions:
        actionable = True
        AcceptedInteractions[entity](value)
        break

  return actionable
