# -*- coding: utf-8 -*-
import pandas as pd
from config import FILE_TYPE
from pathlib import Path
from extract_header import extract_header
import os
       
def get_files(path_,year):
    sts = path_+'/'+str(year)+'/'
    files = {p.resolve() for p in Path(sts).glob("**/*" )if p.suffix in FILE_TYPE}
    
    files = open_files(files,path_,year)
    
#    return files

def open_files(files,path_,year):

    headers = extract_header(path_,year)
    
    for file in sorted(files):
       
        try:
            df = pd.read_table(file,header=None, sep=',')
        except:
            df = pd.read_table(file,header=None, sep='\n')
            df = df[0].str.split(',', expand=True)

        ids = df[0].unique()
#        print(ids)
        #Separate ID
        ddf = {}
        for ids in ids:
            ddf[ids] = pd.DataFrame()
            ddf[ids] = (df.loc[df[0] == ids])
            ddf[ids] = ddf[ids].dropna(axis=1, how='all')
            
            
            
            os.system('cls' if os.name == 'nt' else 'clear')
            for h in range(len(headers)):
                print(headers[h]['name'])
                for k in range(len(headers[h]['variables'])):
                    print(headers[h]['variables'][k][0])
#                    try:
#                        if int(headers[h]['variables'][k][0]) == ddf[ids][0].iloc[0]:
##                    if headers[h]['variables'][k][0] == ddf[ids][0]:
#                            print(headers[h]['variables'][k])
#                    except KeyError:
#                        pass
#            
            
#            print('Processing... File Name:',file)
            
#            locat = ddf[ids][0].iloc[0]
            
#            print(locat)
            print(ddf[ids].head(10))
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
    