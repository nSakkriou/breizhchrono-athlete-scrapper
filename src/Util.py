import time, json
import datetime
import re
import unidecode

def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)

def getId():
    id = str(time.time()).split(".")
    return "".join(id)

def getActualYear():
    today = datetime.date.today()
    return today.year

def loadClubFile(clubPathFile: str):
    with open(clubPathFile, "w+", encoding="utf8") as f:
        data = json.load(f)

        print(data)