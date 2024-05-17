--Still being developed. will refine into a fully automated script when I get it done. 
--CREATE DATABASE Atlas_Duo
--drop database Atlas_Duo
CREATE TABLE User_Storage (
	UserGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
    author varchar(33),
	AuthorId varchar(255) unique, --this comes from discord
    Pronouns varchar(50),
    AutoProxyOn BIT default 0,
    AutoProxyTarget varchar(50),
	CreateDate datetime default GETUTCDATE(),
	LastUpdate datetime default GETUTCDATE()
)

CREATE TABLE USER_NOTES(
	NoteGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	UserGUID UNIQUEIDENTIFIER,
	NoteText VARCHAR(1024),
	SortOrder int,
	CreateDate datetime default GETUTCDATE(),
	LastUpdate datetime default GETUTCDATE()
)

CREATE TABLE User_Groups(
	GroupGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	OwnerID UNIQUEIDENTIFIER,
	DisplayName VarChar(50)
)

CREATE TABLE System_Storage (
	SystemGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	UserGUID UNIQUEIDENTIFIER,
	Pronouns varchar(50),
	CallText varchar(255) not null,
	DisplayName varchar(33),
	ImageURL varchar(255),
	BioGraphy varchar(max),
	PreTag varchar(255),
	PostTag varchar(255),
	createDate datetime default GETUTCDATE(),
	LastUpdate datetime default GETUTCDATE(), --future planning item
	CONSTRAINT SystemUserGUID FOREIGN key (UserGUID) 
	References User_Storage (UserGUID) ON Delete cascade 
	)

CREATE TABLE System_Notes (
	NoteGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	SystemGUID UNIQUEIDENTIFIER,
	NoteText VARCHAR(1024),
	SortOrder int,
	CreateDate datetime default GETUTCDATE(),
	LastUpdate datetime default GETUTCDATE()
	CONSTRAINT SystemNoteGUID FOREIGN key (SystemGUID) 
	References System_Storage (SystemGUID) ON Delete cascade
)

CREATE TABLE System_Groups(
	SystemGUID UNIQUEIDENTIFIER,
	GroupGUID UNIQUEIDENTIFIER,
	Seq int
	CONSTRAINT SystemGUID FOREIGN key (SystemGUID) 
	References System_Storage (SystemGUID) ON Delete cascade,
	CONSTRAINT SystemGroupGUID FOREIGN key (GroupGUID) 
	References User_Groups (GroupGUID) ON Delete cascade,
)


CREATE TABLE MEMBERS (
	MEMBERGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	DisplayName varchar(32),
	Bio varchar(1024)
)

CREATE TABLE MEMBERS_Notes (
	NoteGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	MEMBERSGUID UNIQUEIDENTIFIER,
	NoteText VARCHAR(1024),
	SortOrder int,
	CreateDate datetime default GETUTCDATE(),
	LastUpdate datetime default GETUTCDATE()
	CONSTRAINT MEMBERSNotesGUID FOREIGN key (MEMBERSGUID) 
	References MEMBERS (MEMBERGUID) ON Delete cascade
)

CREATE TABLE Member_Links (
	MemberGUID uniqueidentifier,
	SystemGUID uniqueidentifier,
	createDate datetime default GETUTCDATE(),
	CONSTRAINT MemberGUID FOREIGN key (MemberGUID) 
	References MEMBERS (MEMBERGUID) ON Delete cascade,
	CONSTRAINT MemberSystemGUID FOREIGN key (SystemGUID) 
	References System_Storage (SystemGUID) ON Delete cascade
)

CREATE TABLE MEMBER_GROUPS(
	GroupGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	GroupName varchar(50),
	GroupColor Varchar(10)
)

CREATE TABLE MEMBER_GROUP_lINK(
	LinKGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	GroupGUID UNIQUEIDENTIFIER,
	MemberGUID UNIQUEIDENTIFIER,
	createDate datetime default GETUTCDATE(),
	CONSTRAINT MemberGroupGUID FOREIGN key (GroupGUID) 
	References MEMBER_GROUPS (GroupGUID) ON Delete cascade,
	CONSTRAINT MemberGroupSystemGUID FOREIGN key (MemberGUID) 
	References MEMBERS (MEMBERGUID) ON Delete cascade
)



--Admin controls area

CREATE TABLE AdminServer (
	ServerGUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	isBlackList bit default 0,
	EnableLogging bit default 0,
	LogChannel varchar(50)
)

CREATE TABLE AdminRooms (
	GUID UNIQUEIDENTIFIER PRIMARY KEY default NEWID(),
	ServerGUID UNIQUEIDENTIFIER,
	RoomIdentifier varchar(50)
	CONSTRAINT ServerGUID FOREIGN key (ServerGUID) 
	References AdminServer (ServerGUID) ON Delete cascade, --this comes from at_duo_user.GUID
)




-- Starboard related tables
CREATE TABLE StarboardSettings (
    GUID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ServerGUID UNIQUEIDENTIFIER, -- This comes from AT_Duo_AdminServer.GUID
    StarboardChannel VARCHAR(50),
    StarboardThreshold INT DEFAULT 5 -- Number of stars needed to post to starboard
);

CREATE TABLE StarredMessages (
    GUID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    MessageID VARCHAR(50), -- ID of the message being starred
    ChannelID VARCHAR(50), -- ID of the channel where the message was posted
    UserID VARCHAR(50), -- ID of the user who posted the message
    StarCount INT DEFAULT 0, -- Number of stars the message has received
    CREATEdAt DATETIME DEFAULT GETUTCDATE()
);

CREATE TABLE StarredReactions (
    GUID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    StarredMessageGUID UNIQUEIDENTIFIER, -- This comes from AT_Duo_StarredMessages.GUID
    UserID VARCHAR(50), -- ID of the user who starred the message
    ReactionDate DATETIME DEFAULT GETUTCDATE()
);