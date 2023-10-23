from Athlete import Athlete
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

    def addAthlete(self, athlete: Athlete):
        self.athleteList.append(athlete)
        self.setCount()

        return {"athleteId" : athlete.getId()}
    
    def getAthete(self, athleteId):
        for athlete in self.athleteList:
            if athlete.getId() == athleteId:
                return athlete
            
        return None
    
    def deleteAthlete(self, athleteId):
        for athlete in self.athleteList:
            if athlete.getId() == athleteId:
                self.athleteList.remove(athlete)
                return {"item" : athlete, "info" : "correctly deleted"}
                    
        return {"item" : None, "info" : "not found"}
    
    def toJSON(self):
        dictArgs = self.__dict__
        print(dictArgs)
        dictArgs["athleteList"] = [athlete.toJSON() for athlete in self.athleteList]
        return dictArgs
    
    # --------- #
    def findAthleteWithFirstOrLastName(self, name:str, strict: bool):
        resultsList = []
        for athlete in self.athleteList:

            if strict:
                if athlete.firstName == name or athlete.lastName == name:
                    resultsList.append(athlete)

            else:
                if name in athlete.firstName or name in athlete.lastName:
                    resultsList.append(athlete)

        return resultsList