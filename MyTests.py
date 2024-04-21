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

def DeleteProxy(Author:str,MyName):
    MyTestCommand[Author].RemoveProxy(MyName)
        
AddTestSystem("Test_User","Test_Proxy","MyCall")
print("Item added")
AddTestSystem("Test_User","Test_Proxy","MyCall") #error expected
ItemDeleted = DeleteProxy("Test_User","Test_Proxy") #should work
print(ItemDeleted)
ItemDeleted = DeleteProxy("Test_User","Test_Proxy") #should error
print(ItemDeleted)
AddTestSystem("Test_User","Test_Proxy","MyCall")#should work
DeleteProxy("Test_User","Test_Proxy") #should work
print(ItemDeleted)
AddTestSystem("Test_User","Test_Proxy","MyCall")
DeleteProxy("Test_User","Test_Proxy")
print(ItemDeleted)

#AddTestSystem("Test_User","Test_Proxy","MyCall") #should error
#AddTestSystem("MY_New_User","Test_Proxy","MyCall") #should pass
#AddTestSystem("MyOtherUser","Test_Proxy","MyCall") #should pass
#AddTestSystem("YetAnotherUser","Test_Proxy","MyCall") #should pass

print(MyTestCommand["Test_User"])
#print(MyTestCommand["MY_New_User"])