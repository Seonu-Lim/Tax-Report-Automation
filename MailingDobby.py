#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory,askopenfilename
from tkinter.messagebox import askyesno, showinfo
from configparser import ConfigParser
import os 
import platform
from automate import analyze_pdf,send_mail

if platform.system()=='Darwin' :
    root_dir = "/User/seonwoolim/Desktop/"
elif platform.system()=='Windows' :
    root_dir = os.path.abspath(os.sep)
else :
    raise NotImplementedError


class ConfigGUI:
    def __init__(self, master=None):
        # build ui
        self.frame = ttk.Frame(master)
        self.frame.configure(height=500, padding=30, width=600)
        self.pdf_dir = tk.StringVar()
        self.contacts_path = tk.StringVar()
        self.mail_address_text = ""
        self.password_text = ""
        self.mail_title_text = ""
        self.mail_body_text = ""
        self.wd = None

       # Check path when initializing
        config_dir = os.path.join(root_dir,".mailing_dobby")
        self.config_path = os.path.join(config_dir,"info.cfg")
        if not os.path.exists(config_dir) :
            os.makedirs(config_dir)
        elif os.path.exists(self.config_path) :
            config = ConfigParser()
            config.read(self.config_path,encoding='utf-8')
            self.pdf_dir.set(config['directories']['pdf_directory'])
            self.contacts_path.set(config['directories']['contact_directory'])
            self.mail_address_text = config['login_info']['address']
            self.password_text = config['login_info']['password']
            self.mail_title_text = config['mail_content']['title']
            self.mail_body_text = config['mail_content']['body']

        self.pdf_dir_part()
        self.contacts_path_part()
        self.login_part()
        self.mail_title_part()
        self.mail_body_part()
        self.analyze_button()
        self.send_mail_button()

        # Main widget
        self.frame.place(anchor="nw", x=0, y=0)
        self.mainwindow = self.frame


    def pdf_dir_part(self) :
        # label
        self.label1 = ttk.Label(self.frame)
        self.label1.configure(text='PDF파일위치')
        self.label1.place(anchor="nw", relx=0.0, rely=0.01, x=0, y=0)
        # entry
        self.entry1 = ttk.Entry(self.frame,textvariable=self.pdf_dir)
        self.entry1.place(anchor="nw", relwidth=0.5, relx=0.30, rely=0.01, x=0, y=0)
        # button
        self.button1 = tk.Button(self.frame,command=self.get_pdf_dir)
        self.button1.configure(text='browse')
        self.button1.place(anchor="nw", relx=0.85, x=0, y=0)

    def contacts_path_part(self) :
        # label
        self.label2 = ttk.Label(self.frame)
        self.label2.configure(text='contacts파일선택')
        self.label2.place(anchor="nw", relx=0.0, rely=0.09, x=0, y=0)
        # entry
        self.entry2 = ttk.Entry(self.frame,textvariable=self.contacts_path)
        self.entry2.place(anchor="nw", relwidth=0.5, relx=0.30, rely=0.09, x=0, y=0)
        # button
        self.button2 = tk.Button(self.frame,self.get_contacts_path)
        self.button2.configure(text='browse')
        self.button2.place(anchor="nw", relx=0.85, rely=0.09, x=0, y=0)


    def login_part(self) :

        # Address part
        self.label3 = ttk.Label(self.frame)
        self.label3.configure(text='메일주소')
        self.label3.place(anchor="nw", relx=0.0, rely=0.2, x=0, y=0)
        self.entry3 = ttk.Entry(self.frame)
        self.entry3.insert(tk.END,self.mail_address_text)
        self.entry3.place(anchor="nw", relwidth=0.3, relx=0.11, rely=0.2, x=0, y=0)

        # Password part
        self.label4 = ttk.Label(self.frame)
        self.label4.configure(text='2차인증PW')
        self.label4.place(anchor="nw", relx=0.5, rely=0.2, x=0, y=0)
        self.entry4 = ttk.Entry(self.frame)
        self.entry4.insert(tk.END,self.password_text)
        self.entry4.place(anchor="nw", relwidth=0.3, relx=0.65, rely=0.2, x=0, y=0)

    def mail_title_part(self) :
        # label
        self.label5 = ttk.Label(self.frame)
        self.label5.configure(text='메일제목')
        self.label5.place(anchor="nw", relx=0, rely=0.3, x=0, y=0)

        # entry
        self.entry5 = ttk.Entry(self.frame)
        self.entry5.insert(tk.END,self.mail_title_text)
        self.entry5.place(anchor="nw", relwidth=0.8, relx=0.11, rely=0.3, x=0, y=0)
        
        
    def mail_body_part(self) :
        # label
        self.label7 = ttk.Label(self.frame)
        self.label7.configure(text='메일내용')
        self.label7.place(anchor="nw", relx=0, rely=0.4, x=0, y=0)
        # entry
        self.text1 = tk.Text(self.frame)
        self.text1.insert(tk.END,self.mail_body_text)
        self.text1.configure(height=10, width=50)
        self.text1.place(anchor="nw",relheight=0.5,relwidth=0.8,relx=0.11,rely=0.4,x=0,y=0)

    def analyze_button(self) :
        button3 = ttk.Button(self.frame)
        button3.configure(text='파일분류')
        button3.place(anchor="nw", relx=0.20, rely=0.95, x=0, y=0)

    def send_mail_button(self) :
        button4 = ttk.Button(self.frame)
        button4.configure(text='메일전송')
        button4.place(anchor="nw", relx=0.65, rely=0.95, x=0, y=0)




    def get_contacts_path(self) :
        file_path = askopenfilename(title='contacts.csv 선택')
        self.contacts_path.set(file_path)

    def get_pdf_dir(self) :
        file_dir= askdirectory(title='PDF 취합폴더 선택')
        self.pdf_dir.set(file_dir)

    def analyze(self) :
        self.make_config_file()
        config = ConfigParser()
        config.read(self.config_path,encoding='utf-8')
        self.wd = analyze_pdf(config)
        showinfo("Finished",f"파일 분류가 완료되었습니다. 파일위치 : {self.wd}")
    
    def send(self) :
        self.make_config_file()
        config = ConfigParser()
        config.read(self.config_path,encoding='utf-8')
        send_mail(config,self.wd)
        showinfo("Finished","메일 전송이 완료되었습니다. 전송 실패 내역을 확인하세요.")
        

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
        with open(self.config_path,'w',encoding='utf-8') as f:
            config_obj.write(f)

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    app.run()
