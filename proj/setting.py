import os
import shutil
from configparser import ConfigParser
from tkinter.filedialog import askdirectory,askopenfilename

root = os.path.abspath(os.sep)

def get_configpath() :
    config_dir = os.path.join(root,".mailing_dobby")
    config_path = os.path.join(config_dir,"info.cfg")
    # initialize config dir if not exist
    if not os.path.exists(config_path) :
        os.makedirs(config_dir)
        config_obj = ConfigParser()
        config_obj['directories'] = {
            'pdf_directory' : askdirectory(title="PDF들이 저장되는 위치 선택"),
            'contact_directory' : askopenfilename(title="contacts.csv 위치 선택")
        }
        config_obj['login_info'] = {
            'address' : input("메일주소 입력"),
            'password' : input("2단계 인증 비밀번호 입력")
        }
        config_obj['mail_content'] = {
            'title' : input("메일 제목 입력"),
            'body' : input("메일 내용 붙여넣기 후 enter")
        }
        with open(config_path,'w') as conf :
            config_obj.write(conf)

get_configpath()