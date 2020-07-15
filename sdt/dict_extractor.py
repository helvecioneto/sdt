# -*- coding: utf-8 -*-
from config import DICT_PATH
import glob
import os
import pandas as pd

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

variables = pd.DataFrame()
sensors = pd.DataFrame()

for file in listdir_nohidden(DICT_PATH):
    variables = variables.append(pd.read_excel(file,sheet_name='Tabela-variavel'))
    sensors = sensors.append(pd.read_excel(file,sheet_name='Tabela-sensor'))
    
## Remove DQC variables
variables = variables[~variables['Nome'].str.contains('dqc', case=False)] 
    
def multi_index(df_column):

    mylist = []
    for variab in df_column:
        s = variables[variables['Nome'].str.match(variab, na=False)] 
        idx = s.Nome.first_valid_index()
        s = s.loc[idx] if idx is not None else None        
        try:
            mylist.append((variab, s['Unidade']))
        except:
            if s is None and (variab != 'temp_sfc' and variab != 'prec'):
                mylist.append((variab,'',''))
           
        if variab == 'temp_sfc':
            mylist.append((variab,'°C',''))
            
        if variab == 'prec':
            mylist.append((variab,'mm',''))
    return(mylist)