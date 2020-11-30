import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


class send_Email():
    def __init__(self, mail_host, mail_port, mail_user, mail_pass, sender):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.sender = sender

    def make_mail(self, title, code, receiver):
        mail_msg = """
        <h1>%s</h1>
        <p>%s</p>
        """ % (title, code)
        self.message = MIMEText(mail_msg, "html", "utf-8")
        self.message['From'] = formataddr(["Libary", self.sender])
        self.message['To'] = formataddr(["User", receiver])
        subject = title
        self.message['Subject'] = Header(subject, "utf-8")

    def send(self, receiver, title, code):
        status = 0
        self.make_mail(title, code, receiver)
        try:
            self.smtpObj = smtplib.SMTP_SSL(self.mail_host, self.mail_port)
            self.smtpObj.login(self.mail_user, self.mail_pass)
            self.smtpObj.sendmail(self.sender, [receiver], self.message.as_string())
            self.smtpObj.quit()
            status = 1
        except smtplib.SMTPException as e:
            print("error!")
            print(e)
        return status
