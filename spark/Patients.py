#!/usr/bin/python

from spark import app, authenticate, dispensary_data, db, h
from flask import render_template, request, redirect, url_for, session

@app.route("/patient")
def Patient():
  return redirect(url_for('NewPatient'))

@app.route("/patient/new")
@authenticate
def NewPatient():
  dispensaryData = dispensary_data()
  return render_template('/patient/new.html', dispensary=dispensaryData)

@app.route("/patient/create", methods=['POST'])
@authenticate
def CreatePatient():
  requestData = request.form
  db.CreateUser(requestData['dispensary_name'], requestData['contact_name'],
    requestData['phone'], requestData['address'])
  # TODO Alert to successful creation
  return redirect(url_for('NewPatient'))

@app.route('/dispensary/patients', methods=['GET'])
@authenticate
def ListPatients():
  patients = db.GetPatientsByDispensary(session['username'])
  return render_template('/patient/list.html', patients=patients)

@app.route('/dispensary/patients/approve', methods=['POST'])
@authenticate
def ApprovePatient():
  requestData = request.form
  phone = int(requestData['phone'])
  db.ActivateUser(phone)
  h.send_message(phone, "Your account is active - welcome to Spark!")
  return redirect(url_for('ListPatients'))
