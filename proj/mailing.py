import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class MailSender() :
    def __init__(self,my_address,password) :
        self.from_address = my_address
        self.gmail = smtplib.SMTP("smtp.gmail.com",587)
        self.gmail.ehlo()
        self.gmail.starttls()
        self.gmail.login(my_address,password)
        self.msg = MIMEMultipart('mixed')
        self.to_address = None

    def clear_mail(self) :
        self.msg = MIMEMultipart('mixed') 

    def write_mail(self,to_address,subject,body) :
        self.msg['From'] = self.from_address
        self.msg['To'] = to_address
        self.to_address = to_address
        self.msg['Subject'] = subject
        self.msg.attach(MIMEText(body.replace("\n","<br>"),"html","utf-8"))

    def attach_files(self,file_list : list) :
        for attachment in file_list :
            attach_binary = MIMEBase("application","octect-stream")
            binary = open(attachment,"rb").read()
            attach_binary.set_payload(binary)
            encoders.encode_base64(attach_binary)
            filename = os.path.basename(attachment)
            attach_binary.add_header(
                "Content-Disposition",
                "attachment",
                filename=('utf-8', '', filename)
                )
            self.msg.attach(attach_binary)
    
    def send_mail(self) :
        self.gmail.sendmail(
            self.from_address,
            self.to_address,
            self.msg.as_string()
        )

    def close_connection(self) :
        self.gmail.quit()