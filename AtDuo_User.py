#storage class for the users
#in the database, this will have an ID code, Username, autoproxyenabled, autoproxyTargetID
import uuid
from AtDu_System import *

class AtDuo_User:
    
    ID = ''
    Name = ''
    #__MyUUID = uuid.uuid4() #this will be controlled by the saving mechanism, if it is SQL, mysql, or some other method, let the item doing the saving handle its ID system
    Systems = []
    IsAutoProxy = False
    AutoProxyTarget = None
    
    
    def __init__(self,Author,ID):
        self.Name = Author
        self.ID = ID
        self.Systems = []
        
    def __str__(self):
        myReturnData = f"{self.Name}, SystemCount: {len(self.Systems)}, isAutoProxy: {self.IsAutoProxy}"
        if self.IsAutoProxy == True:
            myReturnData = myReturnData + f", AutoProxyTarget: {self.AutoProxyTarget}"
        return myReturnData
    
    def DoesProxyExist(self,myData):
        ErrorData = {
            'ExistingProxy':False,
            'CallUsed' : False,
            'NameUsed' : False,
            'Success' : False
        }
        MyCode = 0
        for entry in self.Systems:
            if (entry.CallText == myData.CallText or entry.Name == myData.Name):
                ErrorData["ExistingProxy"] = True
            if entry.CallText == myData.CallText:
                ErrorData["CallUsed"] = True
            if entry.Name == myData.Name:
                ErrorData["NameUsed"] = True
        if ErrorData["ExistingProxy"] == False:
            self.Systems.append(myData)
            print("Data Saved")
            print("Your Proxy called " + str(myData.Name) + " has appeared to have been created")
            ErrorData["success"] = True
        return ErrorData
        
    def AddProxy(self,MyName,myCall,ctx = None):
        myData = AtDu_System(MyName,self.Name,myCall)
        if ctx != None:
            if ctx.message.attachments:
                print(ctx.message.attachments[0].url)
                myData.Image = ctx.message.attachments[0].url
        Responsedata = self.DoesProxyExist(myData)
        return Responsedata
        
    def RemoveProxy(self,ProxyName:str):
        ErrorData = {
            "ItemDeleted":False,
            "ItemFound":False,
            'HasError' : False,
            "Entry":None
        }
        for entry in self.Systems:
            print(entry)
            if entry.Name == ProxyName:
                print("Found it")
                print(entry.Name)
                ErrorData["Entry"] = entry
                ErrorData["ItemFound"] = True
        if ErrorData["ItemFound"] == True:
            self.Systems.remove(ErrorData["Entry"])
            print("Item deleted?")
            ErrorData["ItemDeleted"] = True
        return ErrorData
            
    def UpdateProxyName(self,ProxyName,NewName):
        ErrorData = {
            "Updated":False,
            "ItemFound":False,
            'HasError' : False,
            "Entry":None
        }
        for entry in self.Systems:
            print(entry)
            if entry.Name == ProxyName:
                ErrorData["Entry"] = entry
                ErrorData["ItemFound"] = True
        if ErrorData["ItemFound"] == True:
            ErrorData["Entry"].Name = NewName
            ErrorData["Updated"] = True
        return ErrorData
    
    def UpdateProxyImage(self,Proxyname,NewURL):
        ErrorData = {
            "Updated":False,
            "ItemFound":False,
            'HasError' : False,
            "Entry":None
        }
        for entry in self.Systems:
            print(entry)
            if entry.Name == Proxyname:
                ErrorData["Entry"] = entry
                ErrorData["ItemFound"] = True
        if ErrorData["ItemFound"] == True:
            ErrorData["Entry"].Image = NewURL
            ErrorData["Updated"] = True
        return ErrorData
    
    def UpdateProxyCall(self,ProxyName,NewCall):
        ErrorData = {
            "Updated":False,
            "ItemFound":False,
            'HasError' : False,
            "Entry":None
        }
        for entry in self.Systems:
            print(entry)
            if entry.Name == ProxyName:
                #self.Systems.remove(entry.Name)
                ErrorData["Entry"] = entry
                ErrorData["ItemFound"] = True
        if ErrorData["ItemFound"] == True:
            ErrorData["Entry"].CallText = NewCall
            ErrorData["Updated"] = True
        return ErrorData

    def SetAutoProxy(self,Target):
        ErrorData = {
            "Updated":False,
            "ItemFound":False,
            'HasError' : False,
            "Entry":None
        }
        for entry in self.Systems:
            print(entry)
            if entry.Name == Target:
                ErrorData["Entry"] = entry
                ErrorData["ItemFound"] = True
        if ErrorData["ItemFound"] == True:
            self.AutoProxyTarget = ErrorData["Entry"]
            self.IsAutoProxy = True
            ErrorData["Updated"] = True
        return ErrorData
    
    def StopAutoProxy(self):
        self.AutoProxyTarget = None
        self.IsAutoProxy = False