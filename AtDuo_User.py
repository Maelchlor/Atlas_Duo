#storage class for the users
#in the database, this will have an ID code, Username, autoproxyenabled, autoproxyTargetID
import uuid
from AtDu_System import *

class AtDuo_User:
    
    Name = ''
    #__MyUUID = uuid.uuid4()
    Systems = []
    IsAutoProxy = False
    AutoProxyTarget = ''
    
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
        
    def AddProxy(self,MyName,myCall,ctx):
        myData = AtDu_System(MyName,self.Name,myCall)
        if ctx.message.attachments:
            print(ctx.message.attachments[0].url)
            myData.Image = ctx.message.attachments[0].url
        Responsedata = self.DoesProxyExist(myData)
        return Responsedata
        
    def RemoveProxy(self,ProxyName):
        pass