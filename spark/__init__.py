#!/usr/bin/python

from flask            import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_assets     import Environment, Bundle
from flask_login      import LoginManager
from functools        import wraps
from webassets.filter import get_filter
from spark            import Database, Helpers

# Set up app
app = Flask(__name__)
app.secret_key = Helpers.config.get('APP', 'JWT')

login_manager = LoginManager()
login_manager.init_app(app)

db = Database.Access()
h = Helpers

# Assets
assets = Environment(app)
assets.url = app.static_url_path;
assets.directory = app.static_folder;
assets.append_path('spark/assets')
assets.register('general_scss',    Bundle('general.scss',    filters='pyscss', output='general.css'))
assets.register('general_js',      Bundle('general.js',      filters='jsmin',  output='general.js'))
assets.register('dispensary_scss', Bundle('dispensary.scss', filters='pyscss', output='dispensary.css'))
assets.register('dispensary_js',   Bundle('dispensary.js',   filters='jsmin',  output='dispensary.js'))

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

# Main page
@app.route('/')
def Index():
  return render_template('index.html')

# Common helpers
def authenticate(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    if not db.isLoggedIn:
      return redirect(url_for('DispensaryLogin'))
    return f(*args, **kwargs)
  return wrapper

def dispensary_data():
  return db.GetDispensaryFromUsername(session['username'])

# Import main components
from spark import Messaging, Campaigns, Patients, Dispensaries
