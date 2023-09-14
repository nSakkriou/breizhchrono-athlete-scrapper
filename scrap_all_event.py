from dataclasses import dataclass
from scrapper import Scrapper
import click, logging
from scrapper import *
import datetime, time
from mail import Mailer
from config import *

@dataclass
class Race:
    name: str
    url: str
    eventName: str = None

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

        self.baseURL = "https://www.breizhchrono.com"

        super().__init__()

        # Logs
        logging.basicConfig(filename=f'./log/{str(datetime.date.today())}.log', format='%(asctime)s; %(levelname)s; %(message)s', level=logging.INFO, encoding="utf8")
        
        if mail:
            logging.info(f"--------- START : ScrapperEventPage instance (MAIL: ON, EMAIL RECEIVER: {receiver}, CLUB: {club}) ---------")
        else:
            logging.info(f"--------- START : ScrapperEventPage instance (CLUB: {club}) ---------")


    def getAllRace(self):
        logging.info(f"START : ScrapperEventPage method getAllRace")

        soup = self.scrapPage(self.URLEventsList)

        for td in soup.find_all("td", class_="courseName"):
            race = Race(td.find("a").text, self.baseURL + td.find("a")["href"])
            self.raceList.append(race)
            logging.info(f"DURING : ScrapperEventPage method getAllRace : add race ({race.show()})")


        logging.info(f"END : ScrapperEventPage method getAllRace")


    def getUniqueEvent(self):
        logging.info(f"START : ScrapperEventPage method getUniqueEvent")

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
                logging.info(f"DURING : ScrapperEventPage method getUniqueEvent : add unique event ({race.show()})")
                

        logging.info(f"END : ScrapperEventPage method getUniqueEvent")

    def updateDB(self):
        logging.info(f"START : ScrapperEventPage method updateDB")
        logging.info(f"END : ScrapperEventPage method updateDB")
        #Update sqlite DB with new data (singleEventList)

    def launchScriptOnAllEvent(self):
        logging.info(f"START : ScrapperEventPage method launchScriptOnAllEvent")

        for event in self.singleEventList:
            scrap_one_event(event.url, self.club, self.mail, self.receiver)
            logging.info(f"DURING : ScrapperEventPage method launchScriptOnAllEvent : start scrapping event ({event.url})")
            

        logging.info(f"END : ScrapperEventPage method launchScriptOnAllEvent")



    def build(self):
        logging.info(f"START : ScrapperEventPage method build")
        start_time = time.time()

        self.getAllRace()
        self.getUniqueEvent()
        self.updateDB()
        self.launchScriptOnAllEvent()

        total_time_total = time.time() - start_time
        logging.info(f"END : ScrapperEventPage method build : time ({total_time_total})")




def scrap_one_event(lien: str, club: str, mail: bool, receiver: str):
    urls = URLScrapper(lien, club)
    urls.build()

    if mail and urls.filename != "unnamed":
        logging.info(f"START : send mail (receiver: {receiver}, lien: {lien})")
        mailer = Mailer(receiver, urls.filename, urls.eventName, club)
        mailer.setup()
        mailer.sendMail()
        logging.info(f"END : send mail (receiver: {receiver}, lien: {lien})")

@click.command()

@click.option("--club", default=DEFAULT_CLUB, help="Nom du club recherché")
@click.option("--mail", is_flag=True, show_default=True, default=DEFAULT_MAIL_FLAG, help="Envoi de mail ou non")
@click.option("--receiver", default=DEFAULT_MAIL_RECEIVER, help="Email de la personne voulant recevoir les données")
def main(club: str, mail: bool, receiver: str):
    scrapEvent = ScrapperEventPage(club, mail, receiver)
    scrapEvent.build()
    logging.info(f"--------- END : ScrapperEventPage instance ---------")


if __name__ == "__main__":
    main()