# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np


def translate_brb(df):

    ### Meteorological data separete
    id_ = str(int(df.iloc[0][0]))
    meteo = df[[id_,'Year','Day','Min','Temp_sfc', 'Humid', 'Press','Prec','Ws10_AVG','Wd10_AVG','Wd10_STD']]
    meteo['timestamp'] = meteo['Year'].astype(str) +'/' + meteo['Day'].astype(str) + ' ' + pd.to_timedelta(meteo['Min'],unit='m').astype(str).str[-18:-10]
    meteo['timestamp'] = pd.to_datetime(meteo['timestamp'],format='%Y/%j %H:%M:%S')
    meteo = meteo.rename(columns=str.lower)
    meteo = meteo.set_index('timestamp')
    
    meteo = meteo.rename(columns={id_: 'id'})
    
    ## Copy values to create ws10_std
    meteo['ws10_std'] = np.nan
    meteo['ws10_std'] = np.where(meteo.ws10_avg == 3333.0, meteo.ws10_avg, meteo.ws10_std)
    meteo['ws10_std'] = np.where(meteo.ws10_avg == -5555, meteo.ws10_avg, meteo.ws10_std)

    ## Conversion types
    conversion = {'id':'first','year':'first','day':'first','min':'first',
                  'temp_sfc' : 'first', 'humid' : 'first', 'press' : 'first',
                  'prec' : 'sum', 'ws10_avg' : 'mean', 'wd10_avg' : 'median', 'wd10_std': 'std', 'ws10_std':'first' }
    
    ## Mask to not resample this values
    Mask = meteo[(meteo != 3333.0) & (meteo != -5555) & (meteo != np.nan)]
    ## Calculate standard deviation based resample
    Mask['ws10_std'] = Mask.ws10_avg.resample("10min", how=np.std)
    
    ## Apply ressample based conversion
    Mask = Mask.resample('10min',how=conversion)

    ## Final DataFrame
    meteorological = Mask.fillna(meteo)
    meteorological = meteorological.reset_index()
    
    columns = ['id','timestamp','year','day','min','temp_sfc','humid','press','prec',
                                     'ws10_avg','wd10_avg','wd10_std','ws10_std']
    meteorological = meteorological.reindex(columns=columns)


    mux = pd.MultiIndex.from_tuples([('id', '',''),('timestamp', '',''),('year', '',''),('day', '',''),('min', '',''),
                                     ('temp_sfc', 'C','tmo_ventil'), ('humid', '%','tmo_ventil'),('press', 'mb','tmo_ventil'),('prec','mm','tmo_ventil'),
                                     ('ws10_avg', 'm/s','tmo_ventil'),('wd10_avg', 'm/s','tmo_ventil'),('wd10_std', 'deg','tmo_ventil'),('ws10_std', 'm/s','tmo_ventil')])
    
    ### Add multiindex columns
    meteorological.columns = mux
    
    ## Copy dataframe to drop columns
    solar = df.copy()
    
    solar.drop(['Temp_sfc', 'Humid', 'Press','Prec','Ws10_AVG','Wd10_AVG','Wd10_STD','CosAngZen'], axis=1, inplace=True)
    print(solar)

