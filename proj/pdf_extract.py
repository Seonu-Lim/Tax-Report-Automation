import tabula
import os
import shutil

class TaxInfoAnalyzer() :

    def __init__(self,file_path:str) :

        dfs = tabula.read_pdf(file_path,pages='all')

        dfs[1].columns = dfs[1].loc[0,:]
        dfs[1] = dfs[1].drop(0)
        dfs[1] = dfs[1].iloc[:-1,:].set_index('세목명')
        taxes = dfs[1]["납부금액"].str.replace(",","").str.replace(" ","").astype(float)

        self.file_path = file_path
        self.company_name = dfs[0].values[2][1]
        self.taxes = taxes[taxes>0]

    def check_taxlist(self,target_dir) :

        if len(self.taxes)>1 :
            file_dir,file_name = os.path.split(self.file_path)
            target_path = os.path.join(target_dir,file_name)
            shutil.move(self.file_path,target_path)
        else :
            # TODO : check if directory exists
            # if exists, move file
            # else, make directory and move
            pass

            
