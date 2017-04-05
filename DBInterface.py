#!/usr/bin/python2

import psycopg2
import hashlib
import requests
import os
import time
import json
import ConfigParser
import Helpers as h

JWT = h.config.get('DB', 'JWT')
DBUser = h.config.get('DB', 'USER')
DBPass = h.config.get('DB', 'DBPD')
DBHost = h.config.get('DB', 'HOST')
DBName = h.config.get('DB', 'DatabaseName')

class DatabaseAccess(object):
    def __init__(self, DatabaseName=DBName, user=DBUser, password=DBPass, host=DBHost):
        self._conn = psycopg2.connect(database=DatabaseName, user=user, password=password, host=host)
        self._cur = self._conn.cursor()
        self.isLoggedIn = 0

    def Hello(self):
        return "It's working...it's working"

    def InsertDB(self, query):
        self._cur.execute(query)
        self._conn.commit()

    def SaltandHash(self, PD,salt):
        for i in range(100):
            PD = hashlib.sha256(str(PD).encode()).hexdigest()+salt
        return PD

    def AddDispensary(self, DispName, contactName, Email, Phone, Addr, LoginName, PD):
        DispName = DispName.lower()
        contactName = contactName.lower()
        Email = Email.lower()
        Addr = Addr.lower()

        salt = str(int(round(time.time() * 1000)))
        PD = self.SaltandHash(PD,salt)

        self.InsertDB("""INSERT INTO Dispensary values (DEFAULT, '{DispName}', '{Contactname}', '{Contactemail}', {Contactphone}, {Status}, '{Addr}')""".format(DispName=DispName, Contactname=contactName, Contactemail=Email, Contactphone=Phone, Status=True, Addr=Addr))
        self.InsertDB("""INSERT INTO LoginDisp values (DEFAULT, (select DispensaryId from Dispensary where Name='{DispName}'), '{LoginName}', '{PD}', '{Salt}')""".format(DispName=DispName, LoginName=LoginName, PD=PD, Salt=salt))

    def AddInventory(self, DispName, ProductName, Amount):
        DispName = DispName.lower()
        ProductName = ProductName.lower()

        self.InsertDB("""INSERT INTO Inventory values (DEFAULT, select DispensaryId from Dispensary where Name='{DispName}', '{ProductName}', {Amount}, {isAvailable})""".format(DispName=DispName, ProductName=ProductName, Amount=Amount, isAvailable=1))

    def AddUserInfo(self, Username, Userphone, DispName, UserAddr):
        Username = Username.lower()
        DispName = DispName.lower()
        UserAddr = UserAddr.lower()

        self.InsertDB("""INSERT INTO UserInfo values (DEFAULT, '{Username}', {Userphone}, (select DispensaryId from Dispensary where Name='{DispName}'), '{UserAddr}','{SmoochUID}', {isActive})""".format(Username=Username, SmoochUID=hashlib.sha256(str(Userphone).encode()).hexdigest(), Userphone=Userphone, DispName=DispName, UserAddr=UserAddr, isActive=False))

    def AddOrder(self, Userphone, DispName):
        DispName = DispName.lower()

        self.InsertDB("""INSERT INTO Order values (DEFAULT, select UserId from UserInfo where Userphone={Userphone}, select DispensaryId from Dispensary where Name="{DispName}")""".format(Userphone=Userphone, DispName=DispName))

    def GetSmoochUID(self, Userphone):
        query = """SELECT SmoochUserID from UserInfo where Userphone='{Userphone}'""".format(Userphone=Userphone)
        return self.SelectDB(query)

    def GetDispensaryInfoFromUserPhone(self, Userphone):
        query = """SELECT dispensaryid, name from Dispensary where dispensaryid = (select dispensaryid from UserInfo where Userphone={Userphone})""".format(Userphone=Userphone)
        print query
        return self.SelectDB(query)

    def GetUserId(self, Userphone):
        query = """SELECT SmoochUserId from UserInfo where Userphone={Userphone}""".format(Userphone=Userphone)
        return self.SelectDB(query)

    def SelectDB(self, query):
        self._cur.execute(query)
        return self._cur.fetchall()

    def InitUser(self, Userphone):
        Smooch = self.GetSmoochUID(Userphone)
        headers = {
                    'content-type': 'application/json',
                    'authorization': 'Bearer {CannaKey}'.format(CannaKey=JWT),
                  }

        data = {}
        data['userId'] = Smooch[0][0]
        data = json.dumps(data)
        resp = requests.post('https://api.smooch.io/v1/appusers', headers=headers, data=data)
        print resp.status_code, resp.text

        data={}
        data['type'] = "twilio"
        data['phoneNumber'] = "+"+str(Userphone)
        data = json.dumps(data)
        resp = requests.post('https://api.smooch.io/v1/appusers/{SmoochUID}/channels'.format(SmoochUID=Smooch[0][0]), headers=headers, data=data)
        print resp.status_code, resp.text


    def TextUser(self, Userphone, message):
        Smooch = self.GetSmoochUID(Userphone)
        headers = {
                'content-type': 'application/json',
                'authorization': 'Bearer {CannaKey}'.format(CannaKey=JWT),
                  }

        data = {}
        data['role'] = "appMaker"
        data['type'] = "text"
        data['text'] = message
        data = json.dumps(data)

        resp = requests.post('https://api.smooch.io/v1/appusers/{SmoochUID}/messages'.format(SmoochUID=Smooch[0][0]), headers=headers, data=data)
        print resp.status_code

    def GetPhoneNumberForDisp(self, username):
        query = """SELECT userphone from UserInfo where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{LoginName}')""".format(LoginName = username)
        phoneList = self.SelectDB(query)
        return phoneList 

    def GetUnactivatedUser(self, LoginName):
        query = """SELECT username, userphone from UserInfo where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{LoginName}') and isActive is false""".format(LoginName = LoginName)
        unActiveUsers = self.SelectDB(query)
        print unActiveUsers
        return unActiveUsers

    def UpdateUserToActive(self, phonenumber):
        query = """Update UserInfo Set isActive = True where Userphone={Userphone}""".format(Userphone=phonenumber)
        self.InsertDB(query)

    def Authenticate(self, LoginName, PD):
        query = """SELECT PD, salt FROM LoginDisp where loginname='{LoginName}'""".format(LoginName=LoginName)
        matchPD, salt = self.SelectDB(query)[0]
        PD = self.SaltandHash(PD, salt)
        if (matchPD == PD):
            self.isLoggedIn=1
        else:
            self.isLoggedIn=0
