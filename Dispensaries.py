#!/usr/bin/python

import Spark
from flask import render_template, request, redirect, url_for, session

Spark.app.route("/Dispensary")
def DispensaryForm():
  return render_template('RegisterDispensaryForm.html')

Spark.app.route('/DispensarySignin', methods=['GET', 'POST'])
def Login():
  return render_template('DispensarySignin.html')

Spark.app.route('/AuthDispensarySignin', methods=['GET', 'POST'])
def AuthLogin():
  DispInfo = request.form
  session['username'] = DispInfo['LoginName']
  if DispInfo['LoginName'] == "" or DispInfo['PD'] == "":
    return redirect(url_for('Login'))
  Spark.db.Authenticate(DispInfo['LoginName'], DispInfo['PD'])
  if Spark.db.isLoggedIn:
    return redirect(url_for('DispPage'))
  else:
    return redirect(url_for('Login'))

Spark.app.route("/DispResult", methods=['POST'])
def RegisterDisp():
  DispInfo = request.form
  Spark.db.AddDispensary(DispInfo['name'], DispInfo['contactname'], DispInfo['email'], int(DispInfo['tel']), DispInfo['addr'], DispInfo['LoginName'], DispInfo['PD'])
  return redirect(url_for("Index"))

Spark.app.route('/DispPage', methods=['GET', 'POST'])
Spark.authenticate
def DispPage():
  return render_template('DispensaryPage.html')
