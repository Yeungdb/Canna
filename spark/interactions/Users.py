#!/usr/bin/python

from spark import h
from spark.interactions import Interaction, AcceptedInteractions

class Onboarding(Interaction):

  identifier = "onboarding"

  def __init__(self):
    AcceptedInteractions.update({
      'opt_in_response': self.opt_in_response,
      'opt_out_response': self.opt_out_response,
      'bot_overview': self.bot_overview,
      'opt_out_overview': self.opt_out_overview
    })

  def initial_greeting(self):
    self.respondAndUpdate('initial_greeting', {
      'entity': 'polar_response',
      'values': {
        'yes': 'opt_in_response',
        'no': 'opt_out_response'
      }
    })

  def opt_in_response(self):
    # TODO update user to optedin
    self.respondAndUpdate('opt_in_response', {
      'entity': 'polar_response',
      'values': {
        'yes': 'bot_overview',
        'no': 'opt_out_overview'
      }
    })

  def opt_out_response(self):
    self.respondAndUpdate('opt_out_response')

  def bot_overview(self):
    self.respondAndUpdate('bot_overview')

  def opt_out_overview(self):
    self.respondAndUpdate('opt_out_overview')
