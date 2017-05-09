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

  def Authenticate(self, username, password):
    query = """SELECT PD, salt FROM LoginDisp where loginname='{username}'""".format(username=username)
    matchPD, salt = self.DBSelect(query)[0]
    password = self.SaltandHash(password, salt)
    if (matchPD == password):
      self.isLoggedIn=1
    else:
      self.isLoggedIn=0

  # Dispensaries

  def AddDispensary(self, dispensaryName, contactName, email, phone, address, username, password):
    email = email.lower()
    phone = int(phone)

    salt = str(int(round(time.time() * 1000)))
    password = self.SaltandHash(password, salt)

    self.DBInsert("""INSERT INTO Dispensary values (DEFAULT, '{dispensaryName}', '{address}', '{contactName}', '{email}', {phone}, {status})""".format(dispensaryName=dispensaryName, address=address, contactName=contactName, email=email, phone=phone, status=True))
    self.DBInsert("""INSERT INTO LoginDisp values (DEFAULT, (select DispensaryId from Dispensary where Name='{dispensaryName}'), '{username}', '{password}', '{salt}')""".format(dispensaryName=dispensaryName, username=username, password=password, salt=salt))

  def GetDispensaryFromUsername(self, username):
    query = """SELECT name,address,contactname,contactemail,contactphone from Dispensary where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{LoginName}')""".format(LoginName = username)
    result = self.DBSelect(query)
    return {
      'username': username,
      'name': result[0][0],
      'address': result[0][1],
      'contact_name': result[0][2],
      'contact_email': result[0][3],
      'contact_phone': result[0][4]
    }

  # def GetDispensaryNumbers(self, username):
  #   query = """SELECT userphone from UserInfo where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{LoginName}')""".format(LoginName = username)
  #   phoneList = self.DBSelect(query)
  #   return phoneList

  # Users

  def CreateUser(self, dispensaryName, contactName, phone, address):
    phone = int(phone)
    self.DBInsert("""INSERT INTO UserInfo values (DEFAULT, '{contactName}', {phone}, (select DispensaryId from Dispensary where Name='{dispensaryName}'), '{address}', {isActive})""".format(contactName=contactName, phone=phone, dispensaryName=dispensaryName, address=address, isActive=False))

  def GetPatientsByDispensary(self, username, activeOnly=False):
    query = """SELECT username,userphone,isactive from UserInfo where DispensaryId = (select DispensaryId from LoginDisp where loginname = '{username}') order by isactive""".format(username=username)
    patients = self.DBSelect(query)
    if activeOnly:
      patients = filter(lambda patient: patient[2] == True, patients)
    return patients

  def ActivateUser(self, phone):
    query = """Update UserInfo Set isActive = True where Userphone={phone}""".format(phone=phone)
    self.DBInsert(query)

  def GetUserByNumber(self, phone):
    phone = int(phone)
    query = """SELECT username from UserInfo where Userphone={phone}""".format(phone=phone)
    return self.DBSelect(query)

  # Currently unused

  # def AddInventory(self, DispName, ProductName, Amount):
  #   DispName = DispName.lower()
  #   ProductName = ProductName.lower()

  #   self.DBInsert("""INSERT INTO Inventory values (DEFAULT, select DispensaryId from Dispensary where Name='{DispName}', '{ProductName}', {Amount}, {isAvailable})""".format(DispName=DispName, ProductName=ProductName, Amount=Amount, isAvailable=1))

  # def AddOrder(self, Userphone, DispName):
  #   DispName = DispName.lower()

  #   self.DBInsert("""INSERT INTO Order values (DEFAULT, select UserId from UserInfo where Userphone={Userphone}, select DispensaryId from Dispensary where Name="{DispName}")""".format(Userphone=Userphone, DispName=DispName))

  # def GetDispensaryInfoFromUserPhone(self, Userphone):
  #   query = """SELECT dispensaryid, name from Dispensary where dispensaryid = (select dispensaryid from UserInfo where Userphone={Userphone})""".format(Userphone=Userphone)
  #   return self.DBSelect(query)
