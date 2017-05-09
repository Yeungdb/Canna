#!/usr/bin/python

from spark import app, authenticate, dispensary_data, db
from flask import render_template, request, redirect, url_for, session

@app.route('/dispensary', methods=['GET'])
@authenticate
def DispensaryHome():
  dispensaryData = dispensary_data()
  return render_template('/dispensary/home.html', dispensary=dispensaryData)

@app.route('/dispensary/login', methods=['GET'])
def DispensaryLogin():
  return render_template('/dispensary/login.html')

@app.route('/dispensary/logout')
@authenticate
def DispensaryLogout():
  session.pop('username', None)
  db.isLoggedIn = 0
  return redirect(url_for('Index'))

@app.route('/dispensary/auth', methods=['POST'])
def DispensaryAuth():
  requestData = request.form
  session['username'] = requestData['username']
  if requestData['username'] == "" or requestData['password'] == "":
    return redirect(url_for('Login'))
  db.Authenticate(requestData['username'], requestData['password'])
  if db.isLoggedIn:
    return redirect(url_for('DispensaryHome'))
  else:
    return redirect(url_for('DispensaryLogin'))

@app.route("/dispensary/new", methods=['GET'])
def NewDispensary():
  return render_template('/dispensary/new.html')

@app.route("/dispensary/create", methods=['POST'])
def CreateDispensary():
  requestData = request.form
  # TODO Check for username conflicts
  db.AddDispensary(requestData['dispensary_name'], requestData['contact_name'], requestData['email'],
    requestData['phone'], requestData['address'], requestData['username'], requestData['password'])
  return redirect(url_for('Index'))
