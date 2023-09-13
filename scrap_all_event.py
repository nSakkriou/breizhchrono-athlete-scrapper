from dataclasses import dataclass
from scrapper import Scrapper
import click, logging
from scrapper import *
import datetime, time
from mail import Mailer

@dataclass
class Race:
    name: str
    url: str

    def splitAndRecompose(self):
        temp = self.name.split(" - ")
        self.eventName = temp[0]
        self.name = " - ".join(temp[1:])

    def show(self):
        return self.name, self.url, self.eventName

class ScrapperEventPage(Scrapper):
    
    def __init__(self, club: str, mail: bool, receiver: str) -> None:
        self.URLEventsList = "https://www.breizhchrono.com/liste-des-courses.php"
        self.raceList: [Race] = []
        self.singleEventList: [Race] = []

        self.club = club
        self.mail = mail
        self.receiver = receiver

        super().__init__()

    def getAllRace(self):
        soup = self.scrapPage(self.URLEventsList)

        for td in soup.find_all("td", class_="courseName"):
            self.raceList.append(Race(td.find("a").text, td.find("a")["href"]))

    def getUniqueEvent(self):
        for race in self.raceList:
            race.splitAndRecompose()

        for race in self.raceList:
            
            flag = True
            for event in self.singleEventList:

                if(race.eventName == event.eventName):
                    flag = False
                    break

                # Add compare to sqlite DB

            if flag:
                self.singleEventList.append(race)

    def updateDB(self):
        pass
        #Update sqlite DB with new data (singleEventList)

    def launchScriptOnAllEvent(self):
        for event in self.singleEventList:
            scrap_one_event(event.url, self.club, self.mail, self.receiver)


    def build(self):
        self.getAllRace()
        self.getUniqueEvent()
        self.updateDB()
        self.launchScriptOnAllEvent()

def scrap_one_event(lien: str, club: str, mail: bool, receiver: str):
    start_time = time.time()
    today = str(datetime.date.today())

    logging.basicConfig(filename=f'./log/{today}.log', format='%(asctime)s; %(levelname)s; %(message)s', level=logging.INFO, encoding="utf8")

    logging.info(f"**Started with param (lien: {lien}, club: {club})**")
    urls = URLScrapper(lien, club)
    urls.build()

    total_time_scrapping = time.time() - start_time
    logging.info(f"*End scrapping - duration: {total_time_scrapping}*")

    if mail:
        mailer = Mailer(receiver, urls.filename, urls.eventName, club)
        mailer.setup()
        mailer.sendMail()

    total_time_total = time.time() - start_time
    logging.info(f"**End scrapping + mail - duration: {total_time_total}**")

@click.command()

@click.option("--club", default="Rennes triathlon", help="Nom du club recherché")
@click.option("--mail", is_flag=True, show_default=True, default=True, help="Envoi de mail ou non")
@click.option("--receiver", default="nathansakkriou@gmail.com", help="Email de la personne voulant recevoir les données")
def main(club: str, mail: bool, receiver: str):
    scrapEvent = ScrapperEventPage(club, mail, receiver)
    scrapEvent.build()

if __name__ == "__main__":
    main()