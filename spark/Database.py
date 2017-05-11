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

  def SaltAndHash(self, PD,salt):
    for i in range(100):
      PD = hashlib.sha256(str(PD).encode()).hexdigest()+salt
    return PD

  # Authentication

  def Authenticate(self, username, password):
    matchPD, salt = self.DBSelect("""SELECT Password, Salt FROM DispensaryUser WHERE Username='{username}'""".format(username=username))[0]
    password = self.SaltAndHash(password, salt)
    if (matchPD == password):
      self.isLoggedIn=1
    else:
      self.isLoggedIn=0

  # Dispensaries

  def AddDispensary(self, dispensaryName, contactName, email, phone, address, username, password):
    email = email.lower()
    phone = int(phone)

    salt = str(int(round(time.time() * 1000)))
    password = self.SaltAndHash(password, salt)

    self.DBInsert("""INSERT INTO Dispensary VALUES (DEFAULT, '{dispensaryName}', '{address}', '{contactName}', '{email}', {phone}, {active})""".format(dispensaryName=dispensaryName, address=address, contactName=contactName, email=email, phone=phone, active=True))
    self.DBInsert("""INSERT INTO DispensaryUser VALUES (DEFAULT, (SELECT ID FROM Dispensary WHERE Name='{dispensaryName}'), '{username}', '{password}', '{salt}')""".format(dispensaryName=dispensaryName, username=username, password=password, salt=salt))

  def GetDispensaryFromUsername(self, username):
    result = self.DBSelect("""SELECT * FROM Dispensary WHERE ID=(SELECT DispensaryID FROM DispensaryUser WHERE Username='{username}')""".format(username=username))[0]
    return {
      'username': username,
      'name': result[0],
      'address': result[1],
      'contact_name': result[2],
      'contact_email': result[3],
      'contact_phone': result[4],
      'active': result[5],
      'created_at': result[6]
    }

  # Users

  def CreatePatient(self, dispensaryName, contactName, phone, address):
    phone = int(phone)
    self.DBInsert("""INSERT INTO Patient VALUES (DEFAULT, (SELECT ID FROM Dispensary WHERE Name='{dispensaryName}'), '{contactName}', {phone}, '{address}', {active})""".format(contactName=contactName, phone=phone, dispensaryName=dispensaryName, address=address, active=False))

  def ActivatePatient(self, phone):
    self.DBInsert("""UPDATE Patient SET Active = True WHERE Phone={phone}""".format(phone=phone))

  def GetPatientByPhone(self, phone):
    phone = int(phone)
    result = self.DBSelect("""SELECT * FROM Patient WHERE Phone={phone}""".format(phone=phone))
    if not len(result) == 1:
      return False
    result = result[0]
    return {
      'id': result[0],
      'dispensary_id': result[1],
      'name': result[2],
      'phone': result[3],
      'address': result[4],
      'active': result[5],
      'created_at': result[6]
    }

  def GetPatientsByDispensary(self, username, onlyActive=False):
    patients = self.DBSelect("""SELECT Name, Phone, Active, CreatedAt FROM Patient WHERE DispensaryID=(SELECT DispensaryID FROM DispensaryUser WHERE Username='{username}') ORDER BY Active""".format(username=username))
    if onlyActive:
      patients = filter(lambda patient: patient[2] == True, patients)
    return patients
