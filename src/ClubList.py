from AthleteList import AthleteList
from Athlete import Athlete, AthleteSex
from JSONAble import JSONAble
import csv, Util

class ClubList(JSONAble):

    def __init__(self, clubName) -> None:
        self.clubName = clubName

        self.athleteList = AthleteList()

    def addAthelete(self, athlete: Athlete) -> str:
        return self.athleteList.addAthlete(athlete)
    
    def addAthleteWithParam(self, firstName: str, lastName: str, sexe: AthleteSex) -> str:
        return self.addAthelete(Athlete(firstName, lastName, self.clubName, sexe))
    
    def deleteAthlete(self, athleteId: str) -> dict:
        return self.athleteList.deleteAthlete(athleteId)
    
    def getAthlete(self, athleteId: str) -> Athlete:
        return self.athleteList.getAthete(athleteId)
    
    def toJSON(self) -> dict:
        dictArgs = super().toJSON()
        dictArgs["athleteList"] = self.athleteList.toJSON()
        return dictArgs
    
    def save(self):
        path = Util.slugify(self.clubName) + "_clubList.json"
        print(self)

        with open(path, "w", encoding="utf8") as f:
            f.write(self.__str__())
    # --------- #
    
    def findAthleteWithFirstOrLastName(self, name: str, strict: bool):
        return self.athleteList.findAthleteWithFirstOrLastName(name, strict)

    # --------- #

    def exportAthleteResult(self, athleteId):
        pass

    def exportAllSexAthleteResult(self, athleteSex: AthleteSex):
        pass

    def exportAllEventResult(self, eventName: str):
        pass

    def exportAllAthleteResult(self):
        pass

    # --------- #

    def loadAthleteWithCSV(self, csvPath: str):
        athleteCSV = Util.loadCSV(csvPath, False)

        for athlete in athleteCSV:
            aAthlete = Athlete(athlete[0], athlete[1], self.clubName, athlete[2])

            self.addAthelete(aAthlete)

    def loadAthleteAndResultFromResultCSV(self, csvPath: str):
        athleteAndResultCSV = Util.loadCSV(csvPath, True, ",")

        for athleteAndResult in athleteAndResultCSV:
            nomPrenom = Util.parseNomPrenom(athleteAndResult[3])
            
            id = self.addAthleteWithParam(nomPrenom[0], nomPrenom[1] , athleteAndResult[2])["athleteId"]

            if id != None:
                self.getAthlete(id).addResult(athleteAndResult[0], athleteAndResult[1], athleteAndResult[4], athleteAndResult[5], athleteAndResult[6])


if __name__ == "__main__":
    club = ClubList("Rennes Triathlon")
    print(club)

    # club.loadAthleteWithCSV("rennes_tri_sportif.csv")
    club.loadAthleteAndResultFromResultCSV("data/duathlon-du-donjon-2023.csv")

    club.save()