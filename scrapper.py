from bs4 import BeautifulSoup
import os, requests, csv, logging
from dataclasses import dataclass
from slugify import slugify
import datetime
from config import *

class Scrapper:

    i = 0
    def __init__(self) -> None:
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

        Scrapper.i += 1

    def scrapPage(self, URL: str) -> BeautifulSoup:
        response = requests.get(URL, self.headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

@dataclass
class Athlete:
    rank: str
    name: str
    time: str
    race: str
    event: str

    def toList(self):
        return [self.rank, self.name, self.time, self.race, self.event]

class AthleteList:
    
    def __init__(self) -> None:
        self.list: [Athlete] = [Athlete("Classement", "Nom prenom", "Temps", "Nom de la course", "Evenement")]

    def addList2AthleteList(self, athleteList: [Athlete]):
        for athlete in athleteList:
            self.list.append(athlete)

    def toCSV(self):
        year = datetime.date.today().year
        try:
            event_name = self.list[1].event
            nameFile = slugify(event_name + "-" + str(year))
            with open(f"./data/{nameFile}.csv", "w", newline="", encoding="utf8") as file:
                write = csv.writer(file)

                for athlete in self.list:
                    write.writerow(athlete.toList())

        except Exception as e:
            logging.debug("No athlete of club found on this event")

class URLScrapper(Scrapper):

    def __init__(self, URL: str, club: str) -> None:
        self.URL = URL
        self.listURLS:[str] = []
        self.listPageScrappers:[PageScrapper] = []
        self.athleteList: AthleteList = AthleteList()

        domainName = URL.split("/")[0:3]
        self.domainName = "/".join(domainName)

        self.club = club
        self.filename = ""
        self.eventName = ""

        super().__init__()

        logging.info(f"START : URLScrapper instance (lien: {self.URL}, club: {self.club})")


    def scrapURLS(self) -> None:
        """
        Fill self.listURLS with all race links
        return: None
        """
        logging.info(f"START : URLScrapper method scrapURLS")

        soup = self.scrapPage(self.URL)
        

        raceContainer = soup.find("div", id="cop-course-container")
        
        try:
            for a in raceContainer.find_all("a"):
                race_link = self.domainName + a["href"]
                self.listURLS.append(race_link)
                logging.info(f"DURING : URLScrapper method scrapURLS : add race {race_link}")
        except Exception as e:
            logging.warning(f"DURING : URLScrapper method scrapURLS : can't read race container : error {str(e)}")

        logging.info(f"END : URLScrapper method scrapURLS")


    def initPageScrappers(self):
        logging.info(f"START : URLScrapper method initPageScrappers")

        for url in self.listURLS:
            self.listPageScrappers.append(PageScrapper(url, self.club))

        logging.info(f"END : URLScrapper method initPageScrappers")

    def launchPageScrappers(self):
        logging.info(f"START : URLScrapper method launchPageScrappers")
        
        for pageScrapper in self.listPageScrappers:
            pageScrapper.scrapDataAthlete()

        logging.info(f"END : URLScrapper method launchPageScrappers")

    def getAthleteData2CSV(self):
        logging.info(f"START : URLScrapper method getAthleteData2CSV")
        
        for pageScrapper in self.listPageScrappers:
            self.athleteList.addList2AthleteList(pageScrapper.athleteList)

        self.athleteList.toCSV()

        logging.info(f"END : URLScrapper method getAthleteData2CSV")

    def getEventNameandFilename(self):
        logging.info(f"END : URLScrapper method getEventNameandFilename")

        year = datetime.date.today().year

        try:
            self.eventName = self.athleteList.list[1].event
            self.filename = slugify(self.eventName + "-" + str(year))
        
        except Exception as e:
            logging.warning(f"DURING : URLScrapper method getEventNameandFilename : eventName, filename undefinded : No athletes did this race :error : {str(e)}")
            
            self.eventName = "unnamed"
            self.filename = "unnamed"

        logging.info(f"END : URLScrapper method getEventNameandFilename")
     

    def build(self):
        logging.info(f"START : URLScrapper method build")

        self.scrapURLS()
        self.initPageScrappers()
        self.launchPageScrappers()
        self.getAthleteData2CSV()
        self.getEventNameandFilename()

        logging.info(f"END : URLScrapper method build")

        

class PageScrapper(Scrapper):

    def __init__(self, baseURL: str, club: str) -> None:
        self.baseURl = baseURL
        self.researchedURL = baseURL + "/coureur_search/" + "+".join(club.split(" "))
        self.club = club

        self.athleteList: [Athlete] = []

        super().__init__()
        logging.info(f"START : PageScrapper instance (lien: {self.baseURl}, club: {self.club})")

    def scrapDataAthlete(self):
        logging.info(f"START : PageScrapper method scrapDataAthlete : (lien: {self.baseURl}, club: {self.club})")

        soup = self.scrapPage(self.researchedURL)

        try :
            race_event = soup.find_all("h2")[1].text.split(":")[1].split("-")
            race = race_event[1]
            event = race_event[0]
        except Exception as e:
            logging.error(f"DURING : PageScrapper method scrapDataAthlete : (lien: {self.baseURl}, club: {self.club}) : error {str(e)}")

        isEmpty = soup.find("p", id="course-notice")
        if isEmpty:
            logging.info(f"DURING : URLScrapper method scrapURLS : no one of {self.club} do this race ({self.URL})")
        else:
            try:
                for tr in soup.find(id="detail-course").find("tbody").find_all("tr"):

                    try:

                        rank = tr.find("td", class_="col--classementGlobal").find("a").find("span").text.strip()
                        name = tr.find("td", class_="col--name").find("a").text.strip()
                        time = tr.find("td", class_="col--time").find("a").text.strip()

                        self.athleteList.append(Athlete(rank, name, time, race, event))
                    except Exception as e:
                        logging.error(f"DURING : PageScrapper method scrapDataAthlete : error find data : URL {self.baseURl} : error message: {str(e)}")

            except Exception as e:
                slug = slugify(self.baseURl)

                if PAGE_ERROR_FLAG:
                    logging.warning(f"DURING : PageScrapper method scrapDataAthlete : error find table : check ./errors_pages/{slug}.html : URL {self.baseURl} : error message: {str(e)}")

                    with open(f"./errors_pages/{slug}.html", "w", encoding="utf8") as f:
                        f.write(str(soup))
                else:
                    logging.warning(f"DURING : PageScrapper method scrapDataAthlete : error find table : error message: {str(e)}")

        logging.info(f"END : PageScrapper method scrapDataAthlete")



    
