#!/usr/bin/python

from spark import h
from spark.interactions import Interaction, AcceptedInteractions

class Enquiries(Interaction):

  identifier = "order_enquiry"

  def __init__(self):
    AcceptedInteractions.update({
      'greetings': self.greeting
    })

  def greeting(self, value):
    self.respondAndUpdate('greeting')
