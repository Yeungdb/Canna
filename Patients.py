#!/usr/bin/python

import Spark
from flask import render_template, request, redirect, url_for, session 

Spark.app.route("/Patient")
def PatientForm():
  return render_template('RegisterPatientForm.html')

Spark.app.route("/PatientResult", methods=['POST'])
def RegisterPatient():
  PatientInfo = request.form
  Spark.db.AddUserInfo(PatientInfo['patientname'], PatientInfo['tel'], PatientInfo['dispensaryname'], PatientInfo['addr'])
  return redirect(url_for("Index"))

Spark.app.route('/OnPressApprove', methods=['GET', 'POST'])
def OnPressApprove():
  phoneNumber = int(json.dumps(request.get_data())[1:-1])
  Spark.db.InitUser(phoneNumber)
  DispId, DispName = db.GetDispensaryInfoFromUserPhone(phoneNumber)[0]
  Spark.db.UpdateUserToActive(phoneNumber)
  return h.send_message(phoneNumber, "Your account is active")

Spark.app.route('/ApproveUsers', methods=['GET', 'POST'])
Spark.authenticate
def Approval():
  data = Spark.db.GetUnactivatedUser(session['username'])
  return render_template('Approval.html', result=data)
