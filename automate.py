import os
import pandas as pd
import configparser
from proj.pdf_extract import *
from proj.mailing import MailSender

def run(config) :

    # Initialize and set working directory
    address_dict = pd.read_csv(config['directories']['contact_directory'])[['Name','E-mail 1 - Value']].set_index("Name")['E-mail 1 - Value'].to_dict()
    files = [os.path.join(config['directories']['pdf_directory'],f) for f in os.listdir(config['directories']['pdf_directory']) if f.endswith(".pdf")]
    
    # Split files and update file list
    for file in files :
        split_file(file)
    files = [os.path.join(config['directories']['pdf_directory'],f) for f in os.listdir(config['directories']['pdf_directory']) if f.endswith(".pdf")]
    
    wd = initialize_working_directory(config['directories']['pdf_directory'])

    # Classify pdf files by corporate names
    for file in files :
        try :
            tia = TaxInfoAnalyzer(file)
            move_file(tia,wd)
        except Exception as e:
            print(f"Unable to move file. Exception Detail : {e}")
        
    # get corp lists from pdf files
    corps = os.listdir(wd)

    # Initialize MailSender
    sender = MailSender(config['login_info']['address'],config['login_info']['password'])
    # loop corp lists
    for corp in corps :
        if corp == "CHECK_PLEASE" :
            pass
        elif corp in address_dict :
            to_address = address_dict[corp]
            sender.clear_mail()
            sender.write_mail(
                to_address,
                config['mail_content']['title'],
                config['mail_content']['body']
            )
            files = [os.path.join(os.path.join(wd,corp),i) for i in os.listdir(os.path.join(wd,corp))]
            sender.attach_files(files)
            sender.send_mail()
            print(f"Successfully sent mail to {corp}.")
        else :
            print(f"No such corporate name as {corp} in csv file. Passing...")