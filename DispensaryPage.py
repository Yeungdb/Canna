#!/usr/bin/python

from flask import Flask, render_template, request
app = Flask(__name__)

import DBInterface as DBI
db = DBI.DatabaseAccess()

@app.route("/")
def DispensaryForm():
    return render_template('RegisterDispensaryForm.html')

@app.route("/DispResult", methods=['POST'])
def RegisterDisp():
    DispInfo = request.form
    print DispInfo
    db.AddDispensary(DispInfo['name'], DispInfo['contactname'], DispInfo['email'], int(DispInfo['tel']))
    return DispensaryForm()

if __name__ == "__main__":
    app.run()
