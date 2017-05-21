#!/usr/bin/python

from spark import h
from spark.interactions import Interaction, AcceptedInteractions

class Dispensary(Interaction):

  identifier = "dispensary_help"

class Bot(Interaction):

  identifier = "bot_help"
