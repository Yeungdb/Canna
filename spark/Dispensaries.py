#!/usr/bin/python

from spark import app, authenticate, db
from flask import render_template, request, redirect, url_for, session

@app.route("/Dispensary")
def DispensaryForm():
  return render_template('RegisterDispensaryForm.html')

@app.route('/DispensarySignin', methods=['GET', 'POST'])
def Login():
  return render_template('DispensarySignin.html')

@app.route('/AuthDispensarySignin', methods=['GET', 'POST'])
def AuthLogin():
  DispInfo = request.form
  session['username'] = DispInfo['LoginName']
  if DispInfo['LoginName'] == "" or DispInfo['PD'] == "":
    return redirect(url_for('Login'))
  db.Authenticate(DispInfo['LoginName'], DispInfo['PD'])
  if db.isLoggedIn:
    return redirect(url_for('DispPage'))
  else:
    return redirect(url_for('Login'))

@app.route("/DispResult", methods=['POST'])
def RegisterDisp():
  DispInfo = request.form
  db.AddDispensary(DispInfo['name'], DispInfo['contactname'], DispInfo['email'],
    int(DispInfo['tel']), DispInfo['addr'], DispInfo['LoginName'], DispInfo['PD'])
  return redirect(url_for("Index"))

@app.route('/DispPage', methods=['GET', 'POST'])
@authenticate
def DispPage():
  return render_template('DispensaryPage.html')
