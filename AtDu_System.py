#for managing the class for Systems/alts
#store the Discord name, the name of the altar, and the path for the icon
import json

class AtDu_System:
    Name = ''
    Author = ''
    CallText = ''
    Image = ''
    
    
    # def __init__(self,name : str,author : str) -> None:
    #     self.Name = name
    #     self.Author = author
    #     pass

    #using JSON data now
    #used to generate the data for discord. I will add imports as needed. 
    #def GetDiscordProxy():
    #    pass
    
    #for mods requesting who the proxy was called by.
    def GetBaseUser(self):
        return self.author
    
    def UpdateAvatar(self,Image : str):
        self.Image = Image
    
    def getJSONData(self):
        json = {}
        json["username"] = str(self.Name)
        
        if not self.Image or not self.Image == "":
            json["avatar_url"] = self.Image
        return json