#!/usr/bin/python2

import psycopg2
import hashlib
import requests
import os
import time
import json
import ConfigParser
import Helpers

JWT = Helpers.config.get('APP', 'JWT')
DBUser = Helpers.config.get('DB', 'USER')
DBPass = Helpers.config.get('DB', 'DBPD')
DBHost = Helpers.config.get('DB', 'HOST')
DBName = Helpers.config.get('DB', 'DatabaseName')

class Access(object):
  def __init__(self, DatabaseName=DBName, user=DBUser, password=DBPass, host=DBHost):
    self._conn = psycopg2.connect(database=DatabaseName, user=user, password=password, host=host)
    self._cur = self._conn.cursor()
    self.isLoggedIn = 0

  # Common

  def DBInsert(self, query):
    self._cur.execute(query)
    self._conn.commit()

  def DBSelect(self, query):
    self._cur.execute(query)
    return self._cur.fetchall()

  def SaltandHash(self, PD,salt):
    for i in range(100):
      PD = hashlib.sha256(str(PD).encode()).hexdigest()+salt
    return PD

  # Authentication

  def Authenticate(self, LoginName, PD):
    query = """SELECT PD, salt FROM LoginDisp where loginname='{LoginName}'""".format(LoginName=LoginName)
    matchPD, salt = self.DBSelect(query)[0]
    PD = self.SaltandHash(PD, salt)
    if (matchPD == PD):
      self.isLoggedIn=1
    else:
      self.isLoggedIn=0

  # Dispensaries

  def AddDispensary(self, DispName, contactName, Email, Phone, Addr, LoginName, PD):
    DispName = DispName.lower()
    contactName = contactName.lower()
    Email = Email.lower()
    Addr = Addr.lower()

    salt = str(int(round(time.time() * 1000)))
    PD = self.SaltandHash(PD,salt)

    self.DBInsert("""INSERT INTO Dispensary values (DEFAULT, '{DispName}', '{Addr}', '{Contactname}', '{Contactemail}', {Contactphone}, {Status})""".format(DispName=DispName, Contactname=contactName, Contactemail=Email, Contactphone=Phone, Status=True, Addr=Addr))
    self.DBInsert("""INSERT INTO LoginDisp values (DEFAULT, (select DispensaryId from Dispensary where Name='{DispName}'), '{LoginName}', '{PD}', '{Salt}')""".format(DispName=DispName, LoginName=LoginName, PD=PD, Salt=salt))

  def GetDispensaryNumbers(self, username):
    query = """SELECT userphone from UserInfo where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{LoginName}')""".format(LoginName = username)
    phoneList = self.DBSelect(query)
    return phoneList

  # Users

  def AddUserInfo(self, Username, Userphone, DispName, UserAddr):
    Username = Username.lower()
    DispName = DispName.lower()
    UserAddr = UserAddr.lower()

    self.DBInsert("""INSERT INTO UserInfo values (DEFAULT, '{Username}', {Userphone}, (select DispensaryId from Dispensary where Name='{DispName}'), '{UserAddr}','{SmoochUID}', {isActive})""".format(Username=Username, SmoochUID=hashlib.sha256(str(Userphone).encode()).hexdigest(), Userphone=Userphone, DispName=DispName, UserAddr=UserAddr, isActive=False))

  def GetInactivatedUser(self, LoginName):
    query = """SELECT username, userphone from UserInfo where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{LoginName}') and isActive is false""".format(LoginName = LoginName)
    unActiveUsers = self.DBSelect(query)
    return unActiveUsers

  def ActivateUser(self, phonenumber):
    query = """Update UserInfo Set isActive = True where Userphone={Userphone}""".format(Userphone=phonenumber)
    self.DBInsert(query)

  # Currently unused

  def AddInventory(self, DispName, ProductName, Amount):
    DispName = DispName.lower()
    ProductName = ProductName.lower()

    self.DBInsert("""INSERT INTO Inventory values (DEFAULT, select DispensaryId from Dispensary where Name='{DispName}', '{ProductName}', {Amount}, {isAvailable})""".format(DispName=DispName, ProductName=ProductName, Amount=Amount, isAvailable=1))

  def AddOrder(self, Userphone, DispName):
    DispName = DispName.lower()

    self.DBInsert("""INSERT INTO Order values (DEFAULT, select UserId from UserInfo where Userphone={Userphone}, select DispensaryId from Dispensary where Name="{DispName}")""".format(Userphone=Userphone, DispName=DispName))

  def GetDispensaryInfoFromUserPhone(self, Userphone):
    query = """SELECT dispensaryid, name from Dispensary where dispensaryid = (select dispensaryid from UserInfo where Userphone={Userphone})""".format(Userphone=Userphone)
    return self.DBSelect(query)
