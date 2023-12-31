import Util
from dataclasses import dataclass
from JSONAble import JSONAble

@dataclass
class Result(JSONAble):
    athleteId: str
    prenom: str
    nom: str
    sexe: str
    classement: str
    classement_sexe: str
    temps: str
    course: str
    evenement: str
    annee = Util.getActualYear()

    def toCSV(self, includeHeader: bool = False):
        if not includeHeader:
            return ";".join(self.__dict__.values())

        return ";".join(self.__dict__.keys()) + "\n" + ";".join(self.__dict__.values())
    
if __name__ == "__main__":
    result = Result("10", "Nathan", "Sakkriou", "homme", "1", "1", "1h00", "Tri M", "Tri Carentan")
    
    print(result)