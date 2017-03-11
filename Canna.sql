create table Dispensary (
   DispenaryID serial primary key not null,
   Name text not null,
   Contactname text not null,
   Contactemail text not null,
   Contactphone integer not null,
   Status boolean not null
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
   Userphone integer not null,
   DispensaryId integer not null,
   UserAddr text not null
);

create table DispOrder (
   TransactionID serial primary key not null,
   UserId integer not null,
   DispensaryId integer not null
);
