#!/usr/bin/python

import os
import json
from spark import h

with open(os.path.join(h.current_path, '../', 'resources', 'responses.json')) as data_file:
  responses = json.load(data_file)

class Interaction(object):

  def __init__(self):
    print("Hello")
