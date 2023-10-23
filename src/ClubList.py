from AthleteList import AthleteList
from Athlete import Athlete, AthleteSex
from JSONAble import JSONAble
import csv, Util

class ClubList(JSONAble):

    def __init__(self, clubName) -> None:
        self.clubName = clubName

        self.athleteList = AthleteList()

    def addAthelete(self, athlete: Athlete):
        return self.athleteList.addAthlete(athlete)
    
    def addAthleteWithParam(self, firstName: str, lastName: str, sexe: AthleteSex):
        return self.addAthelete(Athlete(firstName, lastName, self.clubName, sexe))
    
    def deleteAthlete(self, athleteId: str):
        return self.athleteList.deleteAthlete(athleteId)
    
    def getAthlete(self, athleteId: str):
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

    def findFirstAthleteWithFirstOrLastName(self, name: str, strict: bool):
        try:
            return self.athleteList.findAthleteWithFirstOrLastName(name, strict)[0]
        except:
            return []
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
        with open(csvPath, newline='') as csvfile:
            athleteCSV = csv.reader(csvfile, delimiter=';')

            for athlete in athleteCSV:
                aAthlete = Athlete(athlete[0], athlete[1], self.clubName, athlete[2])

                # Check doublon a faire
                self.addAthelete(aAthlete)

if __name__ == "__main__":
    club = ClubList("Rennes Triathlon")
    #club.loadAthleteWithCSV("rennes_tri_sportif.csv")

    #club.addAthleteWithParam("Nathan", "SAkkriou", AthleteSex.MALE)

    #print(club.athleteList.toJSON())
    club.save()