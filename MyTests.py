import json
import time
import re
import aiohttp
import asyncio
import json
import requests

from AtDu_System import *
from AtDuo_User import *

MyTestCommand = {}


def AddTestSystem(Author:str,MyName,myCall):
    myData = AtDu_System(MyName,Author,myCall)
    if not Author in MyTestCommand:
        MyTestCommand[Author] = AtDuo_User(Author)
    MyTestCommand[Author].AddProxy(MyName,myCall)
    #print("Class created")
    # ErrorData = {
    #     'ExistingProxy':False,
    #     'CallUsed' : False,
    #     'NameUsed' : False
    # }
    # #print(Author)
    # #print(ErrorData)
    # #print(MyTestCommand[Author])
    # for entry in MyTestCommand[Author].Systems:
    #     #print(entry)
    #     print(entry.Author)
    #     #print(entry.CallText)
    #     #print(entry.Name)
    #     if (entry.CallText == myCall or entry.Name == MyName):
    #         ErrorData["ExistingProxy"] = True
    #     if entry.CallText == myCall:
    #         ErrorData["CallUsed"] = True
    #     if entry.Name == MyName:
    #         ErrorData["NameUsed"] = True
    # #print(ErrorData)
    # if ErrorData["ExistingProxy"] == False:
    #     MyTestCommand[Author].Systems.append(myData)
    #     #print("Data Saved")
    #     #print("Your Proxy called " + str(myData.Name) + " has appeared to have been created")
    # else:
    #     print("duplicate")
    #     MyErrorMessage = "Your Proxy called " + str(myData.Name) + " appears to already exist."
    #     if ErrorData["NameUsed"] == True:
    #         MyErrorMessage = MyErrorMessage + " Requested Name in Use."
    #     if ErrorData["CallUsed"] == True:
    #         MyErrorMessage = MyErrorMessage + " Requested Call in Use."
    #     print(MyErrorMessage)
        
        
AddTestSystem("Test_User","Test_Proxy","MyCall")
    #should pass
#AddTestSystem("Test_User","Test_Proxy","MyCall") #should error
AddTestSystem("MY_New_User","Test_Proxy","MyCall") #should pass
AddTestSystem("MyOtherUser","Test_Proxy","MyCall") #should pass
AddTestSystem("YetAnotherUser","Test_Proxy","MyCall") #should pass

print(MyTestCommand["Test_User"])
print(MyTestCommand["MY_New_User"])