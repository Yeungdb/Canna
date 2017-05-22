#!/usr/bin/python

from spark import app, authenticate, dispensary_data, db
from flask import render_template, flash, request, redirect, url_for, session

# Dispensary Home
@app.route('/dispensary', methods=['GET'])
@authenticate
def DispensaryHome():
  dispensaryData = dispensary_data()
  return render_template('/dispensary/home.html', dispensary=dispensaryData)

# Dispensary Login Form
@app.route('/dispensary/login', methods=['GET'])
def DispensaryLogin():
  return render_template('/dispensary/login.html')

# Dispensary Logout
@app.route('/dispensary/logout')
@authenticate
def DispensaryLogout():
  session.pop('username', None)
  db.isLoggedIn = 0
  return redirect(url_for('Index'))

# Dispensary Authentication
@app.route('/dispensary/auth', methods=['POST'])
def DispensaryAuth():
  requestData = request.form
  session['username'] = requestData['username']

  if requestData['username'] == '' or requestData['password'] == '':
    flash('Could not log in', 'error')
    return redirect(url_for('DispensaryLogin'))

  db.Authenticate(requestData['username'], requestData['password'])
  if db.isLoggedIn:
    return redirect(url_for('DispensaryHome'))
  else:
    return redirect(url_for('DispensaryLogin'))

# Create New Dispensary Form
@app.route('/dispensary/new', methods=['GET'])
def NewDispensary():
  return render_template('/dispensary/new.html')

# Create Dispensary
@app.route('/dispensary/create', methods=['POST'])
def CreateDispensary():
  requestData = request.form

  if db.DispensaryExists(requestData['username']):
    flash('Sorry, that dispensary username is taken', 'error')
    return redirect(url_for('NewDispensary'))

  db.AddDispensary(requestData['dispensary_name'], requestData['contact_name'], requestData['email'],
    requestData['phone'], requestData['address'], requestData['username'], requestData['password'])
  flash('Dispensary has been created!', 'success')
  return redirect(url_for('Index'))
