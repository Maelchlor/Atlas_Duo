#SQL Manipulation file
import pyodbc
 
#created as I realized this will be operating async. so if I need more than one...
def ad_GetConnector():
    pycnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=.\\SQLEXPRESS;"
                      "Database=Atlas_Duo;"
                      "Trusted_Connection=yes;")
    return pycnxn

def getUserAutoProxyState(AuthorId):
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT AutoProxyOn,AutoProxyTarget FROM AT_Duo_User where authorid = ''%r''' %(AuthorId)) 
    return cursor.fetchone()

def GetUserData(AuthorId):
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT * FROM AT_Duo_User where authorid = ''%r''' %(AuthorId)) 
    return cursor
    #print('Row count: ' + str(cursor.arraysize))
    #for row in cursor:
    #    print('row = %r' % (row,))

def GetUserProxyPrefix(AuthorID):
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT ad_s.calltext, ad_s.SystemGUID from at_duo_user AD_U join at_duo_system AD_S on AD_U.UserGUID = ad_s.UserGUID where ad_U.authorid = \''+AuthorID+'\'') 
    return cursor

def getSpecificProxy(GUID):
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT * FROM AT_Duo_System where systemGUID = \''+GUID+'\'')
    return cursor

def getUserProxy(AuthorID):
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT * FROM AT_Duo_User where authorid = ''%r''' % (AuthorID)) 
    print('Row count: ' + str(cursor.arraysize))
    for row in cursor:
        print('row = %r' % (row,))
        
def CheckIfProxyExists(CallText,DisplayName,AuthorID):
    MyResult = {
            'ExistingProxy':False,
            'CallUsed' : False,
            'NameUsed' : False
        }
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT ad_s.displayname,ad_s.calltext from at_duo_user AD_U join at_duo_system AD_S on AD_U.UserGUID = ad_s.UserGUID where ad_U.authorid = \''+AuthorID+'\' AND (ad_s.calltext = \'' + CallText + '\' OR ad_s.displayname = \'' + DisplayName + '\' ) ')
    if cursor.rowcount != 0:
        MyResult['ExistingProxy'] = True
        for row in cursor:
            if row[0] == DisplayName:
                MyResult['NameUsed'] = True
            if row[1] == CallText:
                MyResult['CallUsed'] = True
    return MyResult
    
def checkForProxyCall(MessageContent,CallID):
    cursor = ad_GetConnector().cursor()
    cursor.execute('SELECT ad_s.calltext from at_duo_user AD_U join at_duo_system AD_S on AD_U.UserGUID = ad_s.UserGUID where AD_U.authorid = \'' + CallID + '\'')
    if cursor.rowcount == 0:
        print("No item found")
    else:
        for row in cursor:
            if (MessageContent.startswith(row[0])):
                print("Got a hit")
            

def CreateUserData(UserID,User):
    connection = ad_GetConnector()
    #print('insert into AT_Duo_User (author,AuthorId ) values (\''+User+ '\',\''+UserID+'\')')
    connection.cursor().execute('insert into AT_Duo_User (author,AuthorId ) values (\''+User+ '\',\''+UserID+'\')')
    connection.commit()

def CreateProxy(UserID,displayname,ImageUrl,calltext):
    connection = ad_GetConnector()
    #SQLCOmmand = ()'insert into AT_Duo_System (userGUID,DisplayName,ImageURL,Calltext) values ((select userguid from AT_Duo_User where AuthorId =')
    #print('insert into AT_Duo_System (userGUID,DisplayName,ImageURL,Calltext) values ((select userguid from AT_Duo_User where AuthorId = \'' + UserID + '\'), \''+displayname+'\', \''+ImageUrl+'\',\''+ calltext+ '\')')
    connection.cursor().execute('insert into AT_Duo_System (userGUID,DisplayName,ImageURL,Calltext) values ((select userguid from AT_Duo_User where AuthorId = \'' + UserID + '\'), \'' + displayname + '\', \'' + ImageUrl + '\',\'' + calltext + '\')')
    connection.commit()
    
    #print(connection.)
    
def DeleteProxy(UserID,DisplayName):
    connection = ad_GetConnector()
    connection.cursor().execute('delete from AT_Duo_System where Displayname = \''+ DisplayName+ '\' AND userGUID = ((select userguid from AT_Duo_User where AuthorId = \'' + UserID + '\'))')
    connection.commit()
    
def UpdateDisplayName(UserID,CurrentName,UpdatedName):
    connection = ad_GetConnector()
    connection.cursor().execute('update at_duo_system set DisplayName = \'' + UpdatedName + '\' where userGUID = ((select userguid from AT_Duo_User where AuthorId = \'' + UserID + '\') AND Displayname = \'' +CurrentName + '\'')
    connection.commit()
    
def UpdateCallText(UserID,UpdatedCall,CurrentName):
    connection = ad_GetConnector()
    connection.cursor().execute('update at_duo_system set CallText = \'' + UpdatedCall + '\' where userGUID = ((select userguid from AT_Duo_User where AuthorId = \'' + UserID + '\') AND Displayname = \'' +CurrentName + '\'')
    connection.commit()

def UpdateImageURL(UserID,NewImage,CurrentName):
    connection = ad_GetConnector()
    connection.cursor().execute('update at_duo_system set ImageURL = \'' + NewImage + '\' where userGUID = ((select userguid from AT_Duo_User where AuthorId = \'' + UserID + '\') AND Displayname = \'' +CurrentName + '\'')
    connection.commit()

def EnableAutoProxy(UserID,DisplayName):
    ProxyStatus = CheckIfProxyExists('',DisplayName,UserID)
    if ProxyStatus['ExistingProxy'] == True:
        connection = ad_GetConnector()
        connection.cursor().execute('update AT_Duo_User set AutoProxyOn = 1, AutoProxyTarget = (Select SystemGUID from AT_Duo_System WHERE DisplayName = \'' + DisplayName + '\' ) WHERE AuthorID = \'' + UserID + '\'')
        connection.commit()
    
def DisableAutoProxy(UserID):
    connection = ad_GetConnector()
    connection.cursor().execute('update AT_Duo_User set AutoProxyOn = 0, AutoProxyTarget = NULL WHERE AuthorID = \'' + UserID + '\'')
    connection.commit()