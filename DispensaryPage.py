#!/usr/bin/python

from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

import DBInterface as DBI
db = DBI.DatabaseAccess()

@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/Patient")
def PatientForm():
    return render_template('RegisterPatientForm.html')

@app.route("/Dispensary")
def DispensaryForm():
    return render_template('RegisterDispensaryForm.html')

@app.route("/DispensarySignin")
def DispensarySignin():
    return render_template('DispensarySignIn.html')

@app.route("/PatientResult", methods=['POST'])
def RegisterPatient():
    PatientInfo = request.form
    db.AddUserInfo(PatientInfo['patientname'], PatientInfo['tel'], PatientInfo['dispensaryname'], PatientInfo['addr'])
    #Do a pop up say something like, thank you for the registration, you will need to contact dispensary to approve of your account.
    return redirect(url_for("Index"))

@app.route("/DispResult", methods=['POST'])
def RegisterDisp():
    DispInfo = request.form
    print(DispInfo)
    db.AddDispensary(DispInfo['name'], DispInfo['contactname'], DispInfo['email'], int(DispInfo['tel']), DispInfo['addr'], DispInfo['LoginName'], DispInfo['PD'])
    #Do a pop up and say thank you for signing up.
    return redirect(url_for("Index"))

if __name__ == "__main__":
    app.run()
