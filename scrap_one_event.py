import click, logging
from scrapper import *
import datetime, time
from mail import Mailer

@click.command()

@click.option("--lien", default="https://www.breizhchrono.com/detail-de-la-course/triathlonswimrundinardcoted-emeraude-triathlondistanceolympiquegroupeedouarddenis-relais-2023-16400", help="un des liens de la l'événement voulu sur breizh chrono")
@click.option("--club", default="Rennes triathlon", help="Nom du club recherché")
@click.option("--mail", is_flag=True, show_default=True, default=True, help="Envoi de mail ou non")
@click.option("--receiver", default="nathansakkriou@gmail.com", help="Email de la personne voulant recevoir les données")

def main(lien: str, club: str, mail: bool, receiver: str):
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

if __name__ == "__main__":
    main()