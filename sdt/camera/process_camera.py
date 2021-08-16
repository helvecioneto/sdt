# -*- coding: utf-8 -*-
from glob import glob
import pandas as pd
from modules.load_config import load_config
import errno
import os

header = load_config()[0]['SKY_CAMERA']


def process_files(path):

    ### Append all files
    df = pd.DataFrame()
    
    for file_ in sorted(glob(str(path)+'/*.txt')):
        df1 = pd.read_csv(file_, sep="\t", header=None,skiprows=2,skipinitialspace=True)
        df = df.append(df1)

    headers = header[1]

    df['sigla'] = path[-3:]
    df['timestamp'] = df[0].astype(str) + df[1].astype(str)
    df['timestamp'] = pd.to_datetime(df['timestamp'] , format='%Y%m%d%H%M%S')

    df['year'] = df['timestamp'].dt.year
    df['day'] = df['timestamp'].dt.dayofyear
    df['min'] = df['timestamp'].dt.minute
    
    df['BRBG'] = df[3]
    df['CDOC'] = df[4]
    df['thick'] = df[5]
    df['thin'] = df[6]
    df['sun'] = df[7]
    
    
    df = df.drop(columns=[0,1,2,3,4,5,6,7])
    mux = pd.MultiIndex.from_tuples(headers)
    df.columns = mux
  
    groups = df.groupby(pd.Grouper(key='timestamp', freq='M'))
    
    dfs = [group for _,group in groups]
    
    for i in dfs:
        output_path = load_config()[0]['FORMATED_OUT'] + path[-3:] + '/Cobertura_Nuvens/' + str(i['timestamp'].dt.year.unique()[0]) + '/'
        output_file = path[-3:]+'_'+str(i['timestamp'].dt.year.unique()[0])+'_'+str(i['timestamp'].dt.strftime('%m').unique()[0])+'_CD_formatado.csv'

            ### Create dir of output if not exist
        if not os.path.exists(os.path.dirname(output_path)):
            try:
                os.makedirs(os.path.dirname(output_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        output = output_path + output_file
        
        i = i.set_index(['timestamp'])
        i = i.resample('5min').first()
        i = i.reset_index()
        
        tsmp = i['timestamp']
        i.drop(labels=['timestamp'], axis=1, inplace = True)
        i.insert(1, 'timestamp', tsmp)
        i.dropna(inplace=True)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(i)
        input()
        i.to_csv(output,index=False)
        