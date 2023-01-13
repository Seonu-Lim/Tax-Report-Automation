#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory,askopenfilename
from tkinter.messagebox import askyesno
from configparser import ConfigParser
import os 
import platform

from automate import run

if platform.system()=='Darwin' :
    root_dir = "/User/seonwoolim/Desktop/"
elif platform.system()=='Windows' :
    root_dir = os.path.abspath(os.sep)
else :
    raise NotImplementedError

class ConfigGUI:
    def __init__(self, master=None):
        # build ui
        self.mainframe = ttk.Frame(master)
        self.mainframe.configure(height=300, width=500)
        self.pdf_dir = tk.StringVar()
        self.contacts_path = tk.StringVar()
        self.mail_address_text = ""
        self.password_text = ""
        self.mail_title_text = ""
        self.mail_body_text = ""

        # Check path when initializing
        config_dir = os.path.join(root_dir,".mailing_dobby")
        self.config_path = os.path.join(config_dir,"info.cfg")
        if not os.path.exists(config_dir) :
            os.makedirs(config_dir)
        elif os.path.exists(self.config_path) :
            config = ConfigParser()
            config.read(self.config_path)
            self.pdf_dir.set(config['directories']['pdf_directory'])
            self.contacts_path.set(config['directories']['contact_directory'])
            self.mail_address_text = config['login_info']['address']
            self.password_text = config['login_info']['password']
            self.mail_title_text = config['mail_content']['title']
            self.mail_body_text = config['mail_content']['body']

        self.pdf_dir_part()
        self.contacts_path_part()
        self.mail_title_part()
        self.mail_body_part()
        self.login_part()
        self.submit_part()
        self.mainframe.place(anchor="nw", x=0, y=0)

        # Main widget
        self.mainwindow = self.mainframe

    def pdf_dir_part(self) :
        ## label
        self.pdf_path_label = ttk.Label(self.mainframe)
        self.pdf_path_label.configure(text='PDF 파일위치')
        self.pdf_path_label.place(anchor="nw", relx=0.1, rely=0.01, x=0, y=0)
        ## Entry
        self.pdf_file_path_entry = ttk.Entry(self.mainframe,textvariable=self.pdf_dir)
        self.pdf_file_path_entry.place(anchor="nw", relx=0.33, rely=0.01, x=0, y=0)
        ## Button
        self.browse_pdf_path = ttk.Button(self.mainframe,command=self.get_pdf_dir)
        self.browse_pdf_path.configure(text='browse')
        self.browse_pdf_path.place(anchor="nw",relheight=0.08,relwidth=0.13,relx=0.74,rely=0.01,x=0,y=0)

    def contacts_path_part(self) :
        ## label
        self.contacts_path_label = ttk.Label(self.mainframe)
        self.contacts_path_label.configure(text='contacts파일선택')
        self.contacts_path_label.place(anchor="nw", relx=0.1, rely=0.12, x=0, y=0)

        # entry
        self.contacts_entry = ttk.Entry(self.mainframe,textvariable=self.contacts_path)
        self.contacts_entry.place(anchor="nw", relx=0.33, rely=0.12, x=0, y=0)

        # button
        self.browse_contacts = ttk.Button(self.mainframe,command=self.get_contacts_path)
        self.browse_contacts.configure(takefocus=False, text='browse')
        self.browse_contacts.place(anchor="nw",relheight=0.08,relwidth=0.13,relx=0.74,rely=0.12,x=0,y=0)

    def mail_title_part(self):
        ## label
        self.mail_title_label = ttk.Label(self.mainframe)
        self.mail_title_label.configure(text='메일제목')
        self.mail_title_label.place(anchor="nw", relx=0.1, rely=0.31, x=0, y=0)
        ## entry
        self.mail_title_entry = ttk.Entry(self.mainframe)
        self.mail_title_entry.insert(tk.END,self.mail_title_text)
        self.mail_title_entry.configure(justify="left")
        self.mail_title_entry.place(anchor="nw",relwidth=0.71,relx=0.2,rely=0.31,x=0,y=0)

    def mail_body_part(self):
        ## label
        self.mail_body_label = ttk.Label(self.mainframe)
        self.mail_body_label.configure(text='메일내용')
        self.mail_body_label.place(anchor="nw", relx=0.1, rely=0.44, x=0, y=0)
        ## entry
        self.mail_body_entry = tk.Text(self.mainframe)
        self.mail_body_entry.insert(tk.END,self.mail_body_text)
        self.mail_body_entry.configure(height=10, width=50)
        self.mail_body_entry.place(anchor="nw",relwidth=0.71,relheight=0.4,relx=0.2,rely=0.42,x=0,y=0)

    def login_part(self) :
        # Address part
        self.mail_address_entry = ttk.Entry(self.mainframe)
        self.mail_address_entry.insert(tk.END,self.mail_address_text)
        self.mail_address_entry.place(anchor="nw",relwidth=0.28,relx=0.17,rely=0.21,x=0,y=0)
        self.mail_address_label = ttk.Label(self.mainframe)
        self.mail_address_label.configure(text='메일주소')
        self.mail_address_label.place(anchor="nw", relx=0.05, rely=0.21, x=0, y=0)

        # Password part
        self.password_entry = ttk.Entry(self.mainframe)
        self.password_entry.insert(tk.END,self.password_text)
        self.password_entry.place(anchor="nw",relwidth=0.28,relx=0.6,rely=0.21,x=0,y=0)
        self.password_label = ttk.Label(self.mainframe)
        self.password_label.configure(text='2차인증PW')
        self.password_label.place(anchor="nw", relx=0.46, rely=0.21, x=0, y=0)


    def submit_part(self) :
        # 5. submit
        self.submit_button = ttk.Button(self.mainframe,command=self.run_all)
        self.submit_button.configure(text='확인')
        self.submit_button.place(anchor="nw", relx=0.44, rely=0.90, x=0, y=0)

    def get_contacts_path(self) :
        file_path = askopenfilename(title='contacts.csv 선택')
        self.contacts_path.set(file_path)

    def get_pdf_dir(self) :
        file_dir= askdirectory(title='PDF 취합폴더 선택')
        self.pdf_dir.set(file_dir)

    def run_all(self) :
        self.make_config_file()
        answer = askyesno(title='Automation',message='정보가 저장되었습니다. 메일을 보내시겠습니까?')
        if answer :
            config = ConfigParser()
            config.read(self.config_path)
            run(config)
        else :
            root.destroy()
        

    def make_config_file(self) :
        mail_title = self.mail_title_entry.get()
        mail_body = self.mail_body_entry.get("1.0",tk.END)

        config_obj = ConfigParser()
        config_obj['directories'] = {
            'pdf_directory' : self.pdf_file_path_entry.get(),
            'contact_directory' : self.contacts_entry.get()
        }
        config_obj['login_info'] = {
            'address' : self.mail_address_entry.get(),
            'password' : self.password_entry.get()
        }
        config_obj['mail_content'] = {
            'title' : mail_title,
            'body' : mail_body
        }
        with open(self.config_path,'w') as f:
            config_obj.write(f)

    def run(self):
        self.mainwindow.mainloop()

    


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x300+250+100")
    app = ConfigGUI(root)
    app.run()
