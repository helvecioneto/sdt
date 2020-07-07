# -*- coding: utf-8 -*-
import pandas as pd

def translate_brb(df):
    
    ### Meteorological data
    met1 = df.iloc[:, 0:4]
    met2 = df[['Temp_sfc', 'Humid', 'Press','Prec','Ws10_AVG','Wd10_AVG','Wd10_STD']]
    met = pd.concat([met1, met2], axis=1)
    met = met.rename(columns={'110': 'id'})
    
    mux = pd.MultiIndex.from_tuples([('id', '',''),('timestamp', '',''),('Year', '',''),('Day', '',''),('Min', '',''),
                                     ('Temp_sfc', 'C','tmo_ventil'), ('Humid', '%','tmo_ventil'),('Press', 'mb','tmo_ventil'),('Prec','mm','tmo_ventil'),
                                     ('Ws10_AVG', 'm/s','tmo_ventil'),('Wd10_AVG', 'm/s','tmo_ventil'),('Wd10_STD', 'deg','tmo_ventil')])
    
    meteorological = pd.DataFrame(met, columns=mux)
    meteorological = meteorological.rename(columns=str.lower)
    meteorological['hour']  = pd.to_timedelta(meteorological['min'],unit='m').astype(str).str[-18:-10]
    meteorological['timestamp'] = meteorological['year'].astype(str) +'/' + meteorological['day'].astype(str) + ' ' + meteorological['hour']
    meteorological['timestamp'] = pd.to_datetime(meteorological['timestamp'],format='%Y/%j %H:%M:%S')
    meteorological.drop(['hour'], axis=1, inplace=True)

    print(meteorological.dtypes)

    print(meteorological.head(30))

    
    df.drop(['Temp_sfc', 'Humid', 'Press','Prec','Ws10_AVG','Wd10_AVG','Wd10_STD','CosAngZen'], axis=1, inplace=True)
    
    
#    df = df.rename(columns={'110': 'id'})
#    met = met.rename(columns={'110': 'id'})
#    df = df.rename(columns=str.lower)
#    met = met.rename(columns=str.lower)
    
    
#    met2 = pd.DataFrame(met2, columns=cols)
#    print(cols)
    
#    meteorological = pd.DataFrame(met, columns=mux)
#    print(meteorological.head())
#    print(met.head())
    
    input("Select header Enter to continue...")

