#!/usr/bin/python2

import psycopg2
import hashlib
import requests
import os
import time

JWT = os.environ['CANNAKEY'] 

class DatabaseAccess(object):
    def __init__(self, DatabaseName="Canna", user="darien", password="", host="127.0.0.1"):
        self._conn = psycopg2.connect(database=DatabaseName, user=user, password=password, host=host)
        self._cur = self._conn.cursor()

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

    def SelectDB(self, query):
        self._cur.execute(query)
        return self._cur.fetchone()

    def InitUser(self, Userphone):
        Smooch = self.GetSmoochUID(Userphone)
        headers = {
                    'content-type': 'application/json',
                    'authorization': 'Bearer {CannaKey}'.format(CannaKey=JWT),
                  }

        data = '{"userId":"{SmoochUID}".format(SmoochUID=Smooch)}'
        requests.post('https://api.smooch.io/v1/appusers', headers=headers, data=data)

        data = '{"type": "twilio", "phoneNumber": "+{PhoneNumber}".format(PhoneNumber=Userphone)}'
        requests.post('https://api.smooch.io/v1/appusers/%7B%7B{SmoochUID}%7D%7D/channels'.format(SmoochUID=Smooch), headers=headers, data=data)


    def TextUser(self, Userphone, message):
        Smooch = self.GetSmoochUID(Userphone)
        headers = {
                'content-type': 'application/json',
                    'authorization': 'Bearer {CannaKey}'.format(CannaKey=JWT),
                  }

        data = '\n{\n    "role": "appMaker",\n    "type": "text",\n    "text": "{MESSAGE}".format(MESSAGE=message)\n}'

        requests.post('https://api.smooch.io/v1/appusers/{SmoochUID}/messages'.format(SmoochUID=Smooch), headers=headers, data=data)

    def GetUnactivatedUser(self, DispensaryName):
        query = """SELECT username, userphone from UserInfo where DispensaryId = (select DispensaryId from Dispensary where name = '{DispensaryName}') and isActive is false""".format(DispensaryName = DispensaryName)
        unActiveUsers = self.SelectDB(query)
        print query
        print unActiveUsers

    def Authenticate(self, LoginName, PD):
        query = """SELECT PD, salt FROM LoginDisp where loginname='{LoginName}'""".format(LoginName=LoginName)
        matchPD, salt = self.SelectDB(query)
        PD = self.SaltandHash(PD, salt)
        if (matchPD == PD):
            return 1
        else:
            return 0
