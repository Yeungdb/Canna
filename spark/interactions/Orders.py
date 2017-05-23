#!/usr/bin/python

from spark import h
from spark.interactions import Interaction, AcceptedInteractions

class Enquiries(Interaction):

  identifier = "order_enquiry"

  def __init__(self):
    AcceptedInteractions.update({
      'request': self.request,
      'greetings': self.greeting,
      'goodbye': self.goodbye
    })

  def greeting(self, *params):
    self.respondAndUpdate('greeting', messageVariables={
      'name': self.user['name'] if self.user['name'] != "" else "there",
    }, nextAction={
      'entity': 'polar_response',
      'values': {
        'yes': 'request',
        'no': 'goodbye'
      }
    })

  def request(self, *params):
    self.respondAndUpdate('request')

  def goodbye(self, *params):
    self.respondAndUpdate('goodbye')
