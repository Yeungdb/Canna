#!/usr/bin/python

from flask import Flask
app = Flask(__name__)

import DBInterface as DBI
db = DBI.DatabaseAccess()

@app.route("/")
def hello():
    return db.Hello()

if __name__ == "__main__":
    app.run()
