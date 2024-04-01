#for managing the class for Systems/alts
#store the Discord name, the name of the altar, and the path for the icon
import json

class AtDu_System:
    Name = ''
    Author = ''
    CallText = ''
    Image = ''
    
    
    def __init__(self,name,author) -> None:
        self.Name = name
        self.Author = author
        pass

    #using JSON data now
    #used to generate the data for discord. I will add imports as needed. 
    #def GetDiscordProxy():
    #    pass
    
    #for mods requesting who the proxy was called by.
    def GetBaseUser(self):
        return self.author
    
    def UpdateAvatar(self,Image):
        self.Image = Image
    
    def getJSONData(self):
        json = JSON_Data = {
            "username" : self.Name,
        }
        if not self.image or not self.image == "":
            json["avatar_url"] = self.Image
        return json