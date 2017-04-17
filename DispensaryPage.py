#!/usr/bin/python

import os
import json
import requests
import DBInterface as DBI
import Helpers as h
from urlparse import urlparse, urljoin
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify 
from flask_login import LoginManager
from wit import Wit

# To be replaced later with real product data
example_product_data = open(os.path.join(h.current_path, 'templates', 'example_products.json')).read() 

app = Flask(__name__)
app.secret_key = h.config.get('DB', 'JWT')

login_manager = LoginManager()
login_manager.init_app(app)

db = DBI.DatabaseAccess()

def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(db.isLoggedIn)
        if not db.isLoggedIn:
            return redirect(url_for("Login"))
        return f(*args, **kwargs)
    return wrapper

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.errorhandler(404)
def handle404(err):
    return render_template('404.html')

@app.errorhandler(403)
def handle404(err):
    return render_template('403.html')

@app.errorhandler(500)
def handle404(err):
    return render_template('500.html', error=err)

@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/Patient")
def PatientForm():
    return render_template('RegisterPatientForm.html')

@app.route("/Dispensary")
def DispensaryForm():
    return render_template('RegisterDispensaryForm.html')

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

@app.route('/GetProduct')
def GetProduct():
    return example_product_data 

@app.route('/OnPressApprove', methods=['GET', 'POST'])
def OnPressApprove():
    phoneNumber = int(json.dumps(request.get_data())[1:-1])
    db.InitUser(phoneNumber)
    DispId, DispName = db.GetDispensaryInfoFromUserPhone(phoneNumber)[0]
    db.UpdateUserToActive(phoneNumber)
    return h.send_message(phoneNumber, "Your account is active")

@app.route('/DispPage', methods=['GET', 'POST'])
@authenticate
def DispPage():
    return render_template('DispensaryPage.html')

@app.route('/ApproveUsers', methods=['GET', 'POST'])
@authenticate
def Approval():
    data = db.GetUnactivatedUser(session['username'])
    return render_template('Approval.html', result=data)

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
        print phone
        db.TextUser(phone, text)
    return redirect(url_for('DispPage'))

@app.route('/Logout')
@authenticate
def Logout():
    session.pop('username', None)
    db.isLoggedIn = 0
    return redirect(url_for('Index'))

@app.route('/CreateCampaignForm')
@authenticate
def CreateCampaignForm():
    return render_template('CreateCampaign.html')



if __name__ == "__main__":
    app.run()
