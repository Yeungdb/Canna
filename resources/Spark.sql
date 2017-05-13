SET TIME ZONE 'UTC';

drop table if exists Dispensary;
drop table if exists DispensaryUser;
drop table if exists Patient;
drop table if exists Interaction;
drop table if exists Campaign;
drop table if exists Inventory;
drop table if exists PatientOrder;

create table Dispensary (
  ID serial primary key not null,
  Name text not null,
  Address text not null,
  ContactName text not null,
  ContactEmail text not null,
  ContactPhone bigint not null,
  Active boolean not null,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);

create table DispensaryUser (
  ID serial primary key not null,
  DispensaryID integer not null,
  Username text not null,
  Password text not null,
  Salt text not null,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);

create table Patient (
  ID serial primary key not null,
  DispensaryID integer not null,
  Name text,
  Phone bigint not null,
  Address text not null,
  Timezone text not null,
  Active boolean not null,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);

create table Interaction (
  ID serial primary key not null,
  PatientID integer not null,
  StateKey text,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);

create table Campaign (
  ID serial primary key not null,
  DispensaryID integer not null,
  Messages text,
  SentAt timestamp,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);

create table Inventory (
  ID serial primary key not null,
  DispensaryID integer not null,
  ProductName text not null,
  Amount real not null,
  Available boolean not null,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);

create table PatientOrder (
  ID serial primary key not null,
  PatientID integer not null,
  DispensaryID integer not null,
  CreatedAt timestamp not null default (now() at time zone 'UTC')
);
