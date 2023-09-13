import smtplib, ssl, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Mailer:

    def __init__(self, receiver: str, filename: str, event_name: str, club: str) -> None:
        self.sender = "nathansakkriou.newsletter@gmail.com"
        self.password = "awbz yzsa rbve fzdd"

        self.receiver = receiver

        self.smtp_server = "smtp.gmail.com"
        self.port = 465

        self.subject = f"Résultat : {event_name} pour {club}"
        self.message = f"Vous trouverez en pièce jointe les résultats des athlètes de {club} pour l'évenement {event_name}"

        self.filename = "./data/" + filename + ".csv"
    
    def setup(self):
        self.msg = MIMEMultipart()
        self.msg["From"] = self.sender
        self.msg["To"] = self.receiver
        self.msg["Subject"] = self.subject

        self.msg.attach(MIMEText(self.message, "plain"))

        attachment = open(self.filename, "rb")
        attachment_package = MIMEBase("application", "octet-stream")
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header("Content-Disposition", "attachment; filename= " + self.filename.split("/")[2])
        self.msg.attach(attachment_package)

        logging.info(f"email correctly setup (sender: {self.sender}, receiver: {self.receiver})")


    def sendMail(self):        
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            try:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receiver, self.msg.as_string())
                logging.info(f"email send ! (sender: {self.sender}, receiver: {self.receiver})")

            except Exception as e:
                logging.error(f"email not send ! (sender: {self.sender}, receiver: {self.receiver}), error: {str(e)}")
