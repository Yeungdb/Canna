#!/usr/bin/python

from spark import app, authenticate, db
from flask import render_template, request, redirect, url_for, session 

@app.route("/Patient")
def PatientForm():
  return render_template('RegisterPatientForm.html')

@app.route("/PatientResult", methods=['POST'])
def RegisterPatient():
  PatientInfo = request.form
  db.AddUserInfo(PatientInfo['patientname'], PatientInfo['tel'],
    PatientInfo['dispensaryname'], PatientInfo['addr'])
  return redirect(url_for("Index"))

@app.route('/OnPressApprove', methods=['GET', 'POST'])
def OnPressApprove():
  phoneNumber = int(json.dumps(request.get_data())[1:-1])
  db.ActivateUser(phoneNumber)
  return h.send_message(phoneNumber, "Your account is active")

@app.route('/ApproveUsers', methods=['GET', 'POST'])
@authenticate
def Approval():
  data = db.GetInactivatedUser(session['username'])
  return render_template('Approval.html', result=data)
