#!/usr/bin/python

from spark import h, db
from spark.interactions import Interaction, AcceptedInteractions

class Onboarding(Interaction):

  identifier = "onboarding"

  def __init__(self):
    AcceptedInteractions.update({
      'bot_overview': self.bot_overview,
      'opt_out_overview': self.opt_out_overview
    })

  def initial_greeting(self):
    self.respondAndUpdate('initial_greeting', messageVariables={
      'name': self.user['name'] if self.user['name'] != "" else "there",
      'dispensary': self.dispensary['name']
    }, nextAction={
      'entity': 'polar_response',
      'values': {
        'yes': 'bot_overview',
        'no': 'opt_out_overview'
      }
    })

  def bot_overview(self):
    self.respondAndUpdate('bot_overview', messageVariables={
      'dispensary': self.dispensary['name']
    })

  def opt_out_overview(self):
    self.respondAndUpdate('opt_out_overview')
