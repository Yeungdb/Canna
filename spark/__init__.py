#!/usr/bin/python

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify 
from flask_login import LoginManager
import Database
import Helpers

# Set up app
app = Flask(__name__)
app.secret_key = Helpers.config.get('APP', 'JWT')

login_manager = LoginManager()
login_manager.init_app(app)

db = Database.Access()

# Common
def authenticate(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if not db.isLoggedIn:
      return redirect(url_for("Login"))
    return f(*args, **kwargs)
  return wrapper

# Error handlers
@app.errorhandler(404)
def handle404(err):
  return render_template('404.html')

@app.errorhandler(403)
def handle404(err):
  return render_template('403.html')

@app.errorhandler(500)
def handle404(err):
  return render_template('500.html', error=err)

# Common routes
@app.route("/")
def Index():
  return render_template('index.html')

@app.route('/Logout')
@authenticate
def Logout():
  session.pop('username', None)
  db.isLoggedIn = 0
  return redirect(url_for('Index'))

# Import main components
import Campaigns
import Patients
import Dispensaries
