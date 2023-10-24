from JSONAble import JSONAble
from Result import Result

class AthleteSex:
    MALE = "homme"
    FEMALE = "femme"

class Athlete(JSONAble):
    def __init__(self, firstName: str, lastName: str, club: str, sexe: AthleteSex) -> None:
        super().__init__()

        self.lastName = lastName.upper()
        self.firstName = firstName
        self.club = club
        self.countResult = 0
        self.sexe = sexe

        self.resultList = []

    def setCount(self):
        self.count = len(self.resultList)

    def addResult(self, rank, sexRank, time, race, event) -> str:
        self.resultList.append(resultId := Result(self.id, self.firstName, self.lastName, self.sexe, rank, sexRank, time, race, event))
        self.setCount()
        return {"resultId" : resultId}
    
    def deleteResult(self, resultId):
        for res in self.resultList:
            if res.getId() == resultId:
                self.resultList.remove(res)
                self.setCount()
                return {"item" : res, "info" : "correctly deleted"}
            
        return {"item" : None, "info" : "not found"}
            
    def getResult(self, resultId):
        for res in self.resultId:
            if res.getId() == resultId:
                return res
            
        return None
    
    def toJSON(self):
        dictArgs = super().toJSON()
        dictArgs["resultList"] = [res.toJSON() for res in self.resultList]
        return dictArgs
    
if __name__ == "__main__":
    athlete = Athlete("Nathan", "Sakkriou", "Rennes Tri", AthleteSex.MALE)
    print(athlete)

    athlete.addResult("1", "1", "1h00", "Tri S", "Tri Carentan")
    print(athlete)