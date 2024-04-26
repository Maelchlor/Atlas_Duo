#storage class for the users
#in the database, this will have an ID code, Username, autoproxyenabled, autoproxyTargetID
import uuid
from AtDu_System import *

class AtDuo_User:
    
    Name = ''
    #__MyUUID = uuid.uuid4()
    Systems = []
    IsAutoProxy = False
    AutoProxyTarget = None
    
    def __init__(self,Author):
        self.Name = Author
        self.Systems = []
        
    def __str__(self):
        return f"{self.Name}, AutoProxy: {self.AutoProxyTarget}, SystemCount: {len(self.Systems)}"
    
    def DoesProxyExist(self,myData):
        ErrorData = {
            'ExistingProxy':False,
            'CallUsed' : False,
            'NameUsed' : False
        }
        MyCode = 0
        for entry in self.Systems:
            if (entry.CallText == myData.CallText or entry.Name == myData.Name):
                ErrorData["ExistingProxy"] = True
            if entry.CallText == myData.CallText:
                ErrorData["CallUsed"] = True
                MyCode = MyCode | 2
            if entry.Name == myData.Name:
                ErrorData["NameUsed"] = True
                MyCode = MyCode | 4
            print(ErrorData)
        if ErrorData["ExistingProxy"] == False:
            self.Systems.append(myData)
            print("Data Saved")
            print("Your Proxy called " + str(myData.Name) + " has appeared to have been created")
            MyCode = 1
        else:
            print("duplicate")
            MyErrorMessage = "Your Proxy called " + str(myData.Name) + " appears to already exist."
            if ErrorData["NameUsed"] == True:
                MyErrorMessage = MyErrorMessage + " Requested Name in Use."
            if ErrorData["CallUsed"] == True:
                MyErrorMessage = MyErrorMessage + " Requested Call in Use."
            print(MyErrorMessage)
        return MyCode

    # def AddProxy(self,MyName,myCall,ImageURL):
    #     myData = AtDu_System(MyName,self.Name,myCall)
    #     myData.Image = ImageURL
    #     Responsedata = self.DoesProxyExist(myData)
    #     return Responsedata
        
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
                #self.Systems.remove(entry.Name)
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
                #self.Systems.remove(entry.Name)
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
                #self.Systems.remove(entry.Name)
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