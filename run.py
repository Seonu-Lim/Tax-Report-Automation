import os
import pandas as pd
import configparser
from proj.pdf_extract import *
from proj.mailing import MailSender

def run(
    my_address : str,
    my_psw : str,
    contact_filepath : str,
    pdf_filedir : str,
    mail_title : str,
    mail_body : str
    ) :

    # Initialize and set working directory
    address_dict = pd.read_csv(contact_filepath)[['Name','E-mail 1 - Value']].set_index("Name")['E-mail 1 - Value'].to_dict()
    files = [os.path.join(pdf_filedir,f) for f in os.listdir(pdf_filedir) if f.endswith(".pdf")]
    wd = initialize_working_directory(pdf_filedir)

    # Classify pdf files by corporate names
    for file in files :
        tia = TaxInfoAnalyzer(file)
        move_file(tia,wd)

    # get corp lists from pdf files
    corps = os.listdir(wd)

    # Initialize MailSender
    sender = MailSender(my_address,my_psw)
    # loop corp lists
    for corp in corps :
        if corp == "CHECK_PLEASE" :
            pass
        elif corp in address_dict :
            to_address = address_dict[corp]
            sender.clear_mail()
            sender.write_mail(
                to_address,
                mail_title,
                mail_body
            )
            files = [os.path.join(os.path.join(wd,corp),i) for i in os.listdir(os.path.join(wd,corp))]
            sender.attach_files(files)
            sender.send_mail()
            print(f"Successfully sent mail to {corp}.")
        else :
            print(f"No such corporate name as {corp} in csv file. Passing...")

if __name__=="__main__" :
    config = configparser.ConfigParser()
    config.read("./assets/info.cfg")
    run(
        config['login_info']['address'],
        config['login_info']['password'],
        config['directories']['contact_directory'],
        config['directories']['pdf_directory'],
        config['mail_content']['title'],
        config['mail_content']['body']
    )