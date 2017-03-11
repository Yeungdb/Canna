#!/usr/bin/python2

import psycopg2


class DatabaseAccess(object):
    def __init__(self, DatabaseName="Canna", user="darien", password="", host="127.0.0.1"):
        self._conn = psycopg2.connect(database=DatabaseName, user=user, password=password, host=host)
        self._cur = self._conn.cursor()

    def Hello(self):
        return "It's working...it's working"

    def AddDispensary(self, DispName, contactName, Email, Phone):
        self._cur.execute("""INSERT INTO Dispensary values (DEFAULT, {DispName}, {Contactname}, {Contactemail}, {Contactphone}, {Status}""").format(DispName=DispName, Contactname=contactName, Contactemail=Email, Contactphone=Phone, Status=1)

    def AddInventory(self, DispName, ProductName, Amount):
        self._cur.execute("""INSERT INTO Inventory values (DEFAULT, select DispensaryId from Dispensary where Name="{DispName}", {ProductName}, {Amount}, {isAvailable}""").format(DispName=DispName, ProductName=ProductName, Amount=Amount, isAvailable=1)

    def AddUserInfo(self, Username, Userphone, DispName, UserAddr):
        self._cur.execute("""INSERT INTO UserInfo values (DEFAULT, {Username}, {Userphone}, select DispensaryId from Dispensary where Name="{DispName}", {UserAddr}""").format(Username=Username, Userphone=Userphone, DispName=DispName, UserAddr=UserAddr)

    def AddOrder(self, Userphone, DispName):
        self._cur.execute("""INSERT INTO Order values (DEFAULT, select UserId from UserInfo where Userphone={Userphone}, select DispensaryId from Dispensary where Name="{DispName}")""")

