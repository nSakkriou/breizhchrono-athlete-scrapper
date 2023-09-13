from bs4 import BeautifulSoup
import os, requests, csv, logging
from dataclasses import dataclass
from slugify import slugify
import datetime

class Scrapper:

    def __init__(self) -> None:
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

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
        event_name = self.list[1].event
        nameFile = slugify(event_name + "-" + str(year))
        
        with open(f"./data/{nameFile}.csv", "w", newline="", encoding="utf8") as file:
            write = csv.writer(file)

            for athlete in self.list:
                write.writerow(athlete.toList())

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

    def scrapURLS(self) -> None:
        """
        Fill self.listURLS with all race links
        return: None
        """
        soup = self.scrapPage(self.URL)
        
        raceContainer = soup.find("div", id="cop-course-container")
        for a in raceContainer.find_all("a"):
            self.listURLS.append(self.domainName + a["href"])

    def initPageScrappers(self):
        for url in self.listURLS:
            self.listPageScrappers.append(PageScrapper(url, self.club))

    def launchPageScrappers(self):
        for pageScrapper in self.listPageScrappers:
            pageScrapper.scrapDataAthlete()

    def getAthleteData2CSV(self):
        for pageScrapper in self.listPageScrappers:
            self.athleteList.addList2AthleteList(pageScrapper.athleteList)

        self.athleteList.toCSV()

    def getEventNameandFilename(self):
        year = datetime.date.today().year
        self.eventName = self.athleteList.list[1].event
        self.filename = slugify(self.eventName + "-" + str(year))

     

    def build(self):
        logging.info("scrapURLS method start")
        self.scrapURLS()
        
        logging.info("initPageScrappers method start")
        self.initPageScrappers()
        
        logging.info("launchPageScrappers method start")
        self.launchPageScrappers()
        
        logging.info("getAthleteData2CSV method start")
        self.getAthleteData2CSV()

        logging.info("getEventNameandFilename method start")
        self.getEventNameandFilename()
        

class PageScrapper(Scrapper):

    def __init__(self, baseURL: str, club: str) -> None:
        self.baseURl = baseURL
        self.researchedURL = baseURL + "/coureur_search/" + "+".join(club.split(" "))

        self.athleteList: [Athlete] = []

        super().__init__()
        logging.info(f"PageScrapper instance init ({self.baseURl})")

    def scrapDataAthlete(self):
        logging.info(f"PageScrapper scrapDataAthlete start (instance of {self.baseURl})")

        soup = self.scrapPage(self.researchedURL)

        race_event = soup.find_all("h2")[1].text.split(":")[1].split("-")
        race = race_event[1]
        event = race_event[0]

        try:
            for tr in soup.find(id="detail-course").find("tbody").find_all("tr"):
                try:

                    rank = tr.find("td", class_="col--classementGlobal").find("a").find("span").text.strip()
                    name = tr.find("td", class_="col--name").find("a").text.strip()
                    time = tr.find("td", class_="col--time").find("a").text.strip()

                    self.athleteList.append(Athlete(rank, name, time, race, event))
                except Exception as e:
                    logging.error(f"PageScrapper scrapDataAthlete error (find data) (instance of {self.baseURl}) error message: {str(e)}")

        except Exception as e:
            slug = slugify(self.baseURl)
            logging.warning(f"PageScrapper scrapDataAthlete warning (find table), check ./errors_pages/{slug}.html (instance of {self.baseURl}) error message: {str(e)}")

            with open(f"./errors_pages/{slug}.html", "w", encoding="utf8") as f:
                f.write(str(soup))


    