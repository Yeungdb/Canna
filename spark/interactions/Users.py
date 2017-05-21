#!/usr/bin/python

from spark import h
from spark.interactions import Interaction, AcceptedInteractions

class Onboarding(Interaction):

  identifier = "onboarding"

  def __init__(self):
    AcceptedInteractions.update({})

  def initial_greeting(self):
    self.respond('initial_greeting')
