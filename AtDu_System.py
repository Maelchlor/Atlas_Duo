#for managing the class for Systems/alts
#store the Discord name, the name of the altar, and the path for the icon
#in the database, ID, ownerID, Name,Calltext,ImageURL,Pronouns,Bio
#see if you need to add anything else to the systems before you finalize the DB design
import json

class AtDu_System:
    Name = ''
    Author = ''
    CallText = ''
    Image = ''
    Pronouns = ''
    Bio = ''
    
    def __str__(self):
        return f"{self.Author} {self.Name} {self.CallText}"
    
    def __init__(self,name,author,CallText):
         self.Name = name
         self.Author = author
         self.CallText = CallText
    #     pass

    #using JSON data now
    #used to generate the data for discord. I will add imports as needed. 
    #def GetDiscordProxy():
    #    pass
    
    #for mods requesting who the proxy was called by. this might not be necessary if I make this a DB response. I can have it pull from the DB instead. 
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