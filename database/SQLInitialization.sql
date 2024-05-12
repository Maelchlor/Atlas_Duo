--drop database Atlas_duo; --reset command before we regenerate everything
CREATE DATABASE Atlas_Duo;

--begin transaction

--rollback transaction

create Table AT_Duo_User (
	GUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
    author varchar(33),
	AuthorId varchar(255),
    Pronouns varchar(50),
    AutoProxyOn BIT default 0,
    AutoProxyTarget varchar(50),
	createDate datetime default GETUTCDATE()
	)

create table AT_Duo_System (
	GUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	parentUserGUID UNIQUEIDENTIFIER, --this comes from at_duo_user.GUID
	parentSystem UNIQUEIDENTIFIER, --this comes from other items in this same table, this is primarily for organization.
	Pronouns varchar(50),
	CallText varchar(255),
	DisplayName varchar(33),
	ImageURL varchar(255),
	BioGraphy varchar(max),
	PreTag varchar(255),
	PostTag varchar(255)
	)

create table AT_Duo_AdminServer (
	GUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	isBlackList bit default 0,
	EnableLogging bit default 0,
	LogChannel varchar(50)
)

create table AT_DUO_AdminRooms (
	GUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	ServerGUID UNIQUEIDENTIFIER,
	RoomIdentifier varchar(50)
)


--future preparation
--create table AT_Duo_UserServerConfig (
--	GUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
--	ServerID UNIQUEIDENTIFIER,
--	)