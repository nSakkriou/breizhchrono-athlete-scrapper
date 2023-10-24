import time, json
from datetime import *
import re, csv
import unidecode
from uuid import uuid4

def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)

def getId():
    return datetime.now().strftime('%Y%m%d%H%M%S-') + str(uuid4())

def getActualYear():
    today = date.today()
    return today.year

def loadClubFile(clubPathFile: str):
    with open(clubPathFile, "w+", encoding="utf8") as f:
        data = json.load(f)

        print(data)

def loadCSV(pathFile: str, haveHeader: bool, delimiter=";"):
    with open(pathFile, newline="", encoding="utf8") as csvFile:
        resultCSV = csv.reader(csvFile, delimiter=delimiter)
        
        resList = []
        for res in resultCSV:
            if haveHeader:
                haveHeader = False
            else:
                resList.append(res)

        return resList
    
def parseNomPrenom(nomPrenom: str):
    if len(nomPrenomList := nomPrenom.split(" ")) == 2:
        return nomPrenomList
    
    nomPrenomList.reverse()
    prenom = nomPrenomList[0]

    del nomPrenomList[0]
    nomPrenomList.reverse()

    return [prenom, " ".join(nomPrenomList)]