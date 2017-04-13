drop table if exists Dispensary;
drop table if exists LoginDisp;
drop table if exists Inventory;
drop table if exists UserInfo;
drop table if exists DispOrder;

create table Dispensary (
   DispensaryID serial primary key not null,
   Name text not null,
   Address text not null,
   Contactname text not null,
   Contactemail text not null,
   Contactphone bigint not null,
   Status boolean not null
);

create table LoginDisp (
   LoginID serial primary key not null,
   DispensaryID integer not null,
   LoginName text not null,
   PD text not null,
   Salt text not null
);

create table Inventory(
   InventoryId serial primary key not null,
   DispensaryId integer not null,
   ProductName text not null,
   Amount real not null,
   isAvailable boolean not null
);

create table UserInfo (
   UserId serial primary key not null,
   Username text,
   Userphone bigint not null,
   DispensaryId integer not null,
   UserAddr text not null,
   SmoochUserId text not null,
   isActive boolean not null
);

create table DispOrder (
   TransactionID serial primary key not null,
   UserId integer not null,
   DispensaryId integer not null
);

-- Why doesn't this login work?
-- insert into Dispensary values (1, 'Acme', '123 Test Street', 'John Doe', 'test@example.com', 1231231234, true);
-- insert into LoginDisp values (1, 1, 'test', 'test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a081492047518550');
