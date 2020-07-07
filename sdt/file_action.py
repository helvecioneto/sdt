# -*- coding: utf-8 -*-
import pandas as pd
from config import FILE_TYPE
from pathlib import Path
from extract_header import extract_header
from translate import translate_station
import os
import logging
       
def get_files(path_,year):
    sts = path_+'/'+str(year)+'/'
    files = {p.resolve() for p in Path(sts).glob("**/*" )if p.suffix in FILE_TYPE}
    
    files = open_files(files,path_,year)
    
#    return files

def open_files(files,path_,year):

    ##Headers from path and year
    headers = extract_header(path_,year)
    
    ### For file
    for file in sorted(files):
        
        ### check if file is correct, ignore .git, .DS
        if file.name.startswith('.') == False:
            try:
                df = pd.read_table(file,header=None, sep=',')
            except:
                df = pd.read_table(file,header=None, sep='\n')
                df = df[0].str.split(',', expand=True)
            ## ID from stations
            ids = df[0].unique()

            #Separate ID
            ddf = {}
            print(file)
            for ids in ids:
                ddf[ids] = pd.DataFrame()
                ddf[ids] = (df.loc[df[0] == ids])
                ### Remove Nan from columns
                ddf[ids] = ddf[ids].dropna(axis=1, how='all')
                possib_head = []
                possib_head2 = []
                names = []
                os.system('cls' if os.name == 'nt' else 'clear')
                
                for h in range(len(headers)):
                    names.append(headers[h]['name']+headers[h]['datetime'])
                    for k in range(len(headers[h]['variables'])):
                        try:
                            #Lock by ID
                            if int(headers[h]['variables'][k][0]) == int(ddf[ids][0].iloc[0]):
                                possib_head2.append(headers[h]['variables'][k])
                                #Lock by number of columns
                                if len(headers[h]['variables'][k]) == len(ddf[ids].columns):
                                    possib_head.append(headers[h]['variables'][k])
                        except:
                            pass
                
                ### Check if size are diferent
                if len(possib_head) == 0:
                    print('Station: ', file.parent.parent.name ,'\t\tYear: ', file.parent.name, '\t\tFile: ', file.name )
                    print('\n')
                    print(pd.DataFrame(names).to_string(index=True, header=False))

                    print('Attention, number of columns are different!')
                    print('')
                    phead = pd.DataFrame(possib_head2)
                    hedd = phead[phead.duplicated(keep='last')]

                    ## Check if duplicated
                    if len(hedd) == 1 and len(hedd[0]) == len(ddf[ids].columns):
                        ## Convert to lowercase
                        hedd =  hedd.values.tolist()
                        hedd = map(lambda x:x.lower(),hedd[0])
                        ## Fix header
                        ddf[ids].columns = hedd
#                       # Translate
                        translate_station(ddf[ids],file)
                    else:
                        print(pd.DataFrame(possib_head2).to_string(index=True, header=True))
                        print('\n')
                        print(ddf[ids].head(10).iloc[:, : 20].to_string(index=False, header=True))
                        print('Não conseguiu encontrar um FSL correto gerar log')
                        logging.basicConfig(filename='warning.txt', filemode='w',format='%(message)s')
                        message = 'Size of variables are different', file,' for station: ', ids
                        logging.warning(message)
                        input("Select header Enter to continue...")

                ## Check if duplicated values    
                if len(possib_head) == 2:
                    print('Station: ', file.parent.parent.name ,'\t\tYear: ', file.parent.name, '\t\tFile: ', file.name )
                    print('\n')
                    print('FSL Names: ')
                    print('')
                    print(pd.DataFrame(names).to_string(index=True, header=False))
                    print('')
                    phead = pd.DataFrame(possib_head)
                    hedd = phead[phead.duplicated(keep='last')]
                    
                    if len(hedd) == 1:
                        ## Convert to lowercase
                        hedd =  hedd.values.tolist()
                        hedd = map(lambda x:x.lower(),hedd[0])
                        ## Fix header
                        ddf[ids].columns = hedd
                        ## Translate
                        translate_station(ddf[ids],file)

                    else:
                        print('\n')
                        print(pd.DataFrame(possib_head).to_string(index=True, header=True))
                        print('')
                        print('\n')
                        print('Data Frame:')
                        print(ddf[ids].head(10).iloc[:, : 20].to_string(index=False, header=True))
                        print('Não conseguiu encontrar um FSL correto gerar log')
                                        ## Logging
                        logging.basicConfig(filename='warning.txt', filemode='w',format='%(message)s')
                        message = 'Size of variables are different', file,' for station ID: ', ids
                        logging.warning(message)
                        input("Select header Enter to continue...")
                    
                ## Are equal    
                if len(possib_head) == 1:
                    print('Station: ', file.parent.parent.name ,'\t\tYear: ', file.parent.name, '\t\tFile: ', file.name )
                    print('\n')
                    print('FSL Names: ')
                    print(pd.DataFrame(names).to_string(index=False, header=False))
                    print('')
                    print('\n')
                    ## Fix header
                    ddf[ids].columns = possib_head
                    ## Translate
                    translate_station(ddf[ids],file)
        