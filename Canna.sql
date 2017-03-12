create table Dispensary (
   DispensaryID serial primary key not null,
   Name text not null,
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
