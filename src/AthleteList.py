from Athlete import Athlete, AthleteSex
from JSONAble import JSONAble

class AthleteList(JSONAble):
    def __init__(self) -> None:
        self.count = 0
        self.athleteList = []
        self.athleteMapIdName = {}

    def setCount(self):
        self.count = len(self.athleteList)

    def updateMap(self, athlete: Athlete):
        self.athleteMapIdName[athlete.lastName + " " + athlete.firstName] = athlete.getId()

    def removeMap(self, athleteId: str):
        del self.athleteMapIdName[athleteList]

    def addAthlete(self, athlete: Athlete):
        try:
            self.athleteMapIdName[(athlete.lastName + " " + athlete.firstName)]
            return {"athleteId" : None, "info" : "doublons"}
        
        except:
            self.athleteList.append(athlete)
            self.setCount()
            self.updateMap(athlete)

            return {"athleteId" : athlete.getId()}
    
    def getAthete(self, athleteId):
        for athlete in self.athleteList:
            print(athlete)
            if athlete.getId() == athleteId:
                return athlete
            
        return None
    
    def deleteAthlete(self, athleteId):
        for athlete in self.athleteList:
            if athlete.getId() == athleteId:
                self.athleteList.remove(athlete)
                self.removeMap(athlete.getId())
                return {"item" : athlete, "info" : "correctly deleted"}
                    
        return {"item" : None, "info" : "not found"}
    
    def toJSON(self):
        dictArgs = super().toJSON()
        dictArgs["athleteList"] = [athlete.toJSON() for athlete in self.athleteList]
        return dictArgs
    
    # --------- #
    def checkIfNameIsPresent(self, name: str, strict: bool):
        for athleteName in self.athleteMapIdName.keys():

            if strict:
                if athleteName.lower() == name.lower():
                    return self.athleteMapIdName[athleteName]
                
            else:
                if name.lower() in athleteName.lower():
                    return self.athleteMapIdName[athleteName]
                
        return None

    def findAthleteWithFirstOrLastName(self, name:str, strict: bool):
        if id := self.checkIfNameIsPresent(name, strict) != None:
            for athlete in self.athleteList:
                if athlete.getId() == id:
                    return athlete

        return None
    
if __name__ == "__main__":
    athleteList = AthleteList()
    print(athleteList)

    athleteList.addAthlete(Athlete("Nathan", "Sakkriou", "Rennes Tri", AthleteSex.MALE))
    print(athleteList)