#!/usr/bin/python

import os
import json
from spark import h, db

with open(os.path.join(h.current_path, '../', 'resources', 'responses.json')) as data_file:
  responses = json.load(data_file)

AcceptedInteractions = {}

class Interaction(object):

  last_interaction = False

  def respondAndUpdate(self, subject, **params):
    if 'messageVariables' in params:
      messageVariables = params['messageVariables']
    else:
      messageVariables = None

    if 'nextAction' in params:
      nextAction = params['nextAction']
    else:
      nextAction = None

    message = responses[self.identifier][subject]
    if messageVariables:
      message = h.interpolate_message(message, messageVariables)
    h.send_message(self.user['phone'], message)

    if self.last_interaction:
      if nextAction:
        db.UpdateExistingInteraction(self.last_interaction['id'], nextAction)
      else:
        db.DeleteLastInteraction(self.last_interaction['id'])
    elif nextAction:
      db.CreateNewInteraction(self.user['id'], nextAction)

  @classmethod
  def confidentEntities(self, entities, confidence=0.5):
    good_entities = {}

    for entity, values in entities.iteritems():
      confident_values = filter(lambda attrs: attrs['confidence'] > confidence, values)
      good_entities[entity] = map(lambda value: value['value'], confident_values)

    return good_entities

  @classmethod
  def lastInteractionMatch(self, entity):
    interaction = db.GetLastInteraction(self.user)

    if not interaction:
      return False

    state = interaction['state']
    if state['entity'] == entity:
      return interaction
    else:
      return False
