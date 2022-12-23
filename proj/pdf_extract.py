import tabula
import os
import shutil
from datetime import date

class TaxInfoAnalyzer() :

    def __init__(self,file_path:str) :

        dfs = tabula.read_pdf(file_path,pages='all')
        dfs[1].columns = dfs[1].loc[0,:]
        dfs[1] = dfs[1].drop(0)
        dfs[1] = dfs[1].iloc[:-1,:].set_index('세목명')
        taxes = dfs[1]["납부금액"].str.replace(",","").str.replace(" ","").astype(float)

        self.file_path = file_path
        self.company_name = dfs[0].values[2][1].replace("\r","")
        self.taxes = taxes[taxes>0]
        self.multiple_taxes = False
        if len(self.taxes) > 1 :
            self.multiple_taxes = True

def initialize_working_directory(file_dir) :
    date_today = date.today().strftime("%Y%m%d")
    file_dir = os.path.join(file_dir,date_today)

    # initialize today's working directory
    if os.path.exists(file_dir) :
        shutil.rmtree(file_dir)
    os.makedirs(file_dir)

    return file_dir


def move_file(tia:TaxInfoAnalyzer,working_dir) :

    file_path,file_name = os.path.split(tia.file_path)

    # name target dir
    if tia.multiple_taxes :
        target_dir = os.path.join(working_dir,"CHECK_PLEASE")
    else :
        target_dir = os.path.join(working_dir,tia.company_name)
    
    if not os.path.exists(target_dir) :
        os.makedirs(target_dir)

    target_path = os.path.join(target_dir,file_name)

    shutil.copyfile(tia.file_path,target_path)
    

    
    

