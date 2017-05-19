#!/usr/bin/python

from spark import app, authenticate, db
from flask import render_template, request, url_for, session

# New Campaign Form
@app.route('/dispensary/campaigns/new')
@authenticate
def NewCampaign():
  return render_template('campaign/new.html')

# Send Campaign
@app.route('/dispensary/campaigns/send', methods=['GET', 'POST'])
@authenticate
def SendCampaign():
  DispInfo = request.form
  text = DispInfo['message']+"\n"
  for i in range(3):
    i+=1
    NameIndex = 'P%dName'%i
    PriceIndex = 'Price%d'%i
    text += DispInfo[NameIndex] + ": $" + DispInfo[PriceIndex] + "\n"
  phoneList = db.GetDispensaryNumbers(session['username'])
  for phone in phoneList:
    phone = phone[0]
    # Send text to user
  return redirect(url_for('DispensaryHome'))
