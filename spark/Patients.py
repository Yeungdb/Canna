#!/usr/bin/python

import pytz
from spark import app, authenticate, dispensary_data, db, h
from flask import render_template, request, redirect, url_for, session
from spark.interactions.Users import Onboarding

# Patient Redirect
@app.route("/patient")
def Patient():
  return redirect(url_for('NewPatient'))

# Create New Patient Form
@app.route("/patient/new")
@authenticate
def NewPatient():
  dispensaryData = dispensary_data()
  timezones = pytz.all_timezones
  return render_template('/patient/new.html', dispensary=dispensaryData, timezones=timezones)

# Create Patient
@app.route("/patient/create", methods=['POST'])
@authenticate
def CreatePatient():
  requestData = request.form
  # TODO Check for unique phone number
  db.CreatePatient(requestData['dispensary_name'], requestData['contact_name'],
    requestData['phone'], requestData['address'], requestData['timezone'])
  # TODO Alert to successful creation
  return redirect(url_for('NewPatient'))

# List Dispensary Patients
@app.route('/dispensary/patients', methods=['GET'])
@authenticate
def ListPatients():
  patients = db.GetPatientsByDispensary(session['username'])
  return render_template('/patient/list.html', patients=patients)

# Approve Patient
@app.route('/dispensary/patients/approve', methods=['POST'])
@authenticate
def ApprovePatient():
  requestData = request.form

  phone = int(requestData['phone'])
  Onboarding.user = db.GetPatientByPhone(phone)
  db.ActivatePatient(phone)

  onboarding = Onboarding()
  onboarding.initial_greeting()

  # TODO Alert to successful activation
  return redirect(url_for('ListPatients'))
