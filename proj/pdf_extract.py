import tabula
from pypdf import PdfReader, PdfWriter
import os
import shutil
from datetime import date

class TaxInfoAnalyzer() :

    def __init__(self,file_path:str) :

        dfs = tabula.read_pdf(file_path,pages='all')
        self.target_period = dfs[1].columns[1]
        dfs[1].columns = dfs[1].loc[0,:]
        dfs[1] = dfs[1].drop(0)
        dfs[1] = dfs[1].iloc[:-1,:].set_index('세목명')
        taxes = dfs[1]["납부금액"].str.replace(",","").str.replace(" ","").astype(float)

        self.file_path = file_path
        self.company_name = dfs[0].values[2][1].replace("\r","")
        self.taxes = taxes[taxes>0]
        self.due_date = dfs[2].iloc[0,0].split("\r")[1]
        self.multiple_taxes = False
        if len(self.taxes) > 1 :
            self.multiple_taxes = True

def split_file(file_path) :
    reader = PdfReader(file_path)
    if len(reader.pages)>1 :
        for i in range(len(reader.pages)) :
            writer = PdfWriter()
            new_filename = file_path.replace(".pdf",f"_{i}.pdf")
            with open(new_filename,'wb') as fp :
                writer.write(fp)
        os.remove(file_path)


def initialize_working_directory(file_dir) :
    date_today = date.today().strftime("%Y%m%d")
    file_dir = os.path.join(file_dir,date_today)

    # initialize today's working directory
    if os.path.exists(file_dir) :
        shutil.rmtree(file_dir)
    os.makedirs(file_dir)

    return file_dir


def move_file(tia:TaxInfoAnalyzer,working_dir) :
    # name target dir
    if tia.multiple_taxes :
        target_dir = os.path.join(working_dir,"CHECK_PLEASE")
    else :
        target_dir = os.path.join(working_dir,tia.company_name)
    
    if not os.path.exists(target_dir) :
        os.makedirs(target_dir)
    new_file_name = f"{tia.company_name}_{tia.target_period}_부가가치세_납부서_{tia.due_date}"
    target_path = os.path.join(target_dir,new_file_name)
    shutil.copyfile(tia.file_path,target_path)
    

    
    

