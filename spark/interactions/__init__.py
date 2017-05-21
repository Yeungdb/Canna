#!/usr/bin/python

import os
import json
from spark import h, db

with open(os.path.join(h.current_path, '../', 'resources', 'responses.json')) as data_file:
  responses = json.load(data_file)

AcceptedInteractions = {}

class Interaction(object):

  def respond(self, subject):
    message = responses[self.identifier][subject]
    h.send_message(self.user['phone'], message)

  @classmethod
  def confidentEntities(self, entities, confidence=0.5):
    good_entities = {}

    for entity, values in entities.iteritems():
      confident_values = filter(lambda attrs: attrs['confidence'] > confidence, values)
      good_entities[entity] = map(lambda value: value['value'], confident_values)

    return good_entities

  @classmethod
  def lastInteractionMatch(self, entity, value):
    interaction = db.GetLastInteraction(self.user)

    if not interaction:
      return False

    state = interaction['state']
    if state['next_entity'] == entity and state['next_value'] == value:
      return interaction['id']
    else:
      return False

  @classmethod
  def createNew(self, results):
    print("create new")

  @classmethod
  def updateExisting(self, last_id, results):
    print("update existing")
