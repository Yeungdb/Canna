#!/usr/bin/python2

import psycopg2
import hashlib
import requests
import os
import time
import json
import ConfigParser
from spark          import Helpers

JWT    = Helpers.config.get('APP', 'JWT')
DBUser = Helpers.config.get('DB', 'USER')
DBPass = Helpers.config.get('DB', 'DBPD')
DBHost = Helpers.config.get('DB', 'HOST')
DBName = Helpers.config.get('DB', 'DatabaseName')

# Database
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
    self.DBInsert("""INSERT INTO DispensaryUser VALUES (DEFAULT, (SELECT ID FROM Dispensary WHERE Na`me='{dispensaryName}'), '{username}', '{password}', '{salt}')""".format(dispensaryName=dispensaryName, username=username, password=password, salt=salt))

  def GetDispensaryFromUsername(self, username):
    result = self.DBSelect("""SELECT * FROM Dispensary WHERE ID=(SELECT DispensaryID FROM DispensaryUser WHERE Username='{username}')""".format(username=username))[0]
    return {
      'username': username,
      'id': result[0],
      'name': result[1],
      'address': result[2],
      'contact_name': result[3],
      'contact_email': result[4],
      'contact_phone': result[5],
      'active': result[6],
      'created_at': result[7]
    }

  def GetDispensaryFromPatient(self, phone):
    phone = int(phone)
    result = self.DBSelect("""SELECT * FROM Dispensary WHERE ID=(SELECT DispensaryID FROM Patient WHERE Phone='{phone}')""".format(phone=phone))[0]
    return {
      'id': result[0],
      'name': result[1],
      'address': result[2],
      'contact_name': result[3],
      'contact_email': result[4],
      'contact_phone': result[5],
      'active': result[6],
      'created_at': result[7]
    }

  def DispensaryExists(self, username):
    result = self.DBSelect("""SELECT * FROM Dispensary WHERE ID=(SELECT DispensaryID FROM DispensaryUser WHERE Username='{username}')""".format(username=username))
    return len(result) == 1

  # Users
  def CreatePatient(self, dispensaryName, contactName, phone, address, timezone):
    phone = int(phone)
    self.DBInsert("""INSERT INTO Patient VALUES (DEFAULT, (SELECT ID FROM Dispensary WHERE Name='{dispensaryName}'), '{contactName}', '{phone}', '{address}', '{timezone}', {active}, {optedIn})""".format(contactName=contactName, phone=phone, dispensaryName=dispensaryName, address=address, timezone=timezone, active=False, optedIn=False))

  def ActivatePatient(self, phone):
    phone = int(phone)
    self.DBInsert("""UPDATE Patient SET Active = True WHERE Phone={phone}""".format(phone=phone))

  def OptInPatient(self, phone):
    phone = int(phone)
    self.DBInsert("""UPDATE Patient SET OptedIn = True WHERE Phone={phone}""".format(phone=phone))

  def PatientIsOptedIn(self, phone):
    phone = int(phone)
    result = self.DBSelect("""SELECT * FROM Patient WHERE OptedIn={optedIn}""".format(optedIn=True))
    return len(result) == 1;

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
      'timezone': result[5],
      'active': result[6],
      'opted_in': result[7],
      'created_at': result[8]
    }

  def GetPatientsByDispensary(self, username, onlyActive=False):
    patients = self.DBSelect("""SELECT Name, Phone, Active, OptedIn, CreatedAt FROM Patient WHERE DispensaryID=(SELECT DispensaryID FROM DispensaryUser WHERE Username='{username}') ORDER BY Active, CreatedAt""".format(username=username))
    if onlyActive:
      patients = filter(lambda patient: patient[2] == True, patients)
    return patients

  def PatientExists(self, phone):
    phone = int(phone)
    result = self.DBSelect("""SELECT * FROM Patient WHERE Phone={phone}""".format(phone=phone))
    return len(result) == 1

  # Interactions
  def GetLastInteraction(self, user):
    patientID = user['id']
    result = self.DBSelect("""SELECT * FROM Interaction WHERE PatientID={patientID}""".format(patientID=patientID))
    if not len(result) == 1:
      return False
    result = result[0]
    return {
      'id': result[0],
      'patient_id': result[1],
      'state': result[2],
      'created_at': result[3]
    }

  def DeleteLastInteraction(self, user):
    patientID = user['id']
    result = self.DBSelect("""DELETE FROM Interaction WHERE PatientID={patientID}""".format(patientID=patientID))

  def CreateNewInteraction(self, patientID, state):
    state = json.dumps(state)
    self.DBInsert("""INSERT INTO Interaction VALUES (DEFAULT, '{patientID}', '{state}')""".format(patientID=patientID, state=state))

  def UpdateExistingInteraction(self, interactionID, state):
    state = json.dumps(state)
    self.DBInsert("""UPDATE Interaction SET State = '{state}' WHERE ID={interactionID}""".format(state=state, interactionID=interactionID))
