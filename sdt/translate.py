# -*- coding: utf-8 -*-
#from config import SOLAR_DATA
from stations.brb import translate_brb
from config import OUTPUT_PATH
import pandas as pd
import datetime

def translate_station(df,path):
    
    if 'BRB' in str(path):
        data = translate_brb(df)
        print(path)
       
        
        timest = str(data[0]['year'][0])+'/'+str(data[0]['jday'][0])
        year = pd.to_datetime(timest, format='%Y/%j').strftime('%Y')
        month = pd.to_datetime(timest, format='%Y/%j').strftime('%m')

        out = OUTPUT_PATH+str('BRB_')+str(year)+'_'+str(month)+'_MD_formatado.csv'
        data[0].to_csv(out,index=False)
        print(out)
        
        print(data[0])
        input("Select header Enter to continue...")
        print(path)
        timest = str(data[1]['year'][1])+'/'+str(data[0]['jday'][0])
        year = pd.to_datetime(timest, format='%Y/%j').strftime('%Y')
        month = pd.to_datetime(timest, format='%Y/%j').strftime('%m')
        
        out = OUTPUT_PATH+str('BRB_')+str(year)+'_'+str(month)+'_SD_formatado.csv'
        print(out)
        print(data[1])
        data[1].to_csv(out,index=False)
        input("Select header Enter to continue...")
