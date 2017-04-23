#!/usr/bin/python

from spark import app, authenticate, db
from flask import render_template, request, url_for, session 

@app.route('/PublishCampaign', methods=['GET', 'POST'])
@authenticate
def PublishCampaign():
  DispInfo = request.form
  text = DispInfo['message']+"\n"
  for i in range(3):
    i+=1
    NameIndex = 'P%dName'%i
    PriceIndex = 'Price%d'%i
    text += DispInfo[NameIndex] + ": $" + DispInfo[PriceIndex] + "\n"
  phoneList = db.GetPhoneNumberForDisp(session['username'])
  for phone in phoneList:
    phone = phone[0]
    db.TextUser(phone, text)
  return redirect(url_for('DispPage'))

@app.route('/CreateCampaignForm')
@authenticate
def CreateCampaignForm():
  return render_template('CreateCampaign.html')
