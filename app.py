import sys
import smtplib, ssl
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tqdm import tqdm


class App:
    def __init__(self):
        self.email: str = sys.argv[1]
        self.password: str = sys.argv[2]
        self.smtp: str = sys.argv[3]
        self.html_file: str = sys.argv[4]
        self.emails_sent_path: str = sys.argv[5]
        self.subject: str = sys.argv[6]
        self.emails_sent: List[str] = []
        self.get_email_to_send()
        self.server = self.init_email_context()
        for email in tqdm(self.emails_sent):
            self.send_email(email)

    def init_email_context(self):
        context = ssl.create_default_context()
        server = smtplib.SMTP(self.smtp, 587)
        server.starttls(context=context)
        server.login(self.email, self.password)
        return server

    def get_email_to_send(self):
        if ".csv" in self.emails_sent:
            csv_file = open(self.emails_sent_path, "r")
            for line in csv_file:
                self.emails_sent.append(line)
            csv_file.close()
        else:
            self.emails_sent.append(self.emails_sent_path)

    def send_email(self, email):
        with open(self.html_file, "r") as file:
            html = file.read()
        msg = MIMEMultipart("alternative")
        msg["Subject"] = self.subject
        msg["From"] = self.email
        msg["To"] = email
        part = MIMEText(html, "html")
        msg.attach(part)
        self.server.sendmail(self.email, email, msg.as_string())


if __name__ == "__main__":
    App()
