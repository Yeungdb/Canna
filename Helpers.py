#!/usr/bin/python

import os
import ConfigParser

current_path = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(current_path, '.env'))
