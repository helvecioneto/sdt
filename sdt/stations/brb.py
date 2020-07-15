# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from dict_extractor import multi_index

def translate_brb(df):

    # ID of station
    id_ = str(int(df.iloc[0][0]))
    
    ### Meteorological variables
    meteo = df[[id_, 'Year', 'Day', 'Min', 'Temp_sfc', 'Humid',
                'Press', 'Prec', 'Ws10_AVG', 'Wd10_AVG', 'Wd10_STD']]
    
    meteo['timestamp'] = meteo['Year'].astype(str) + '/' + meteo['Day'].astype(
        str) + ' ' + pd.to_timedelta(meteo['Min'], unit='m').astype(str).str[-18:-10]
    meteo['timestamp'] = pd.to_datetime(
        meteo['timestamp'], format='%Y/%j %H:%M:%S')
    meteo = meteo.rename(columns=str.lower)
    meteo = meteo.set_index('timestamp')
    
    # Rename first column
    meteo = meteo.rename(columns={id_: 'id'})
    meteo = meteo.rename(columns={'day': 'jday'})

    # Copy values to create ws10_std
    meteo['ws10_std'] = np.nan
    meteo['ws10_std'] = np.where(
        meteo.ws10_avg == 3333.0, meteo.ws10_avg, meteo.ws10_std)
    meteo['ws10_std'] = np.where(
        meteo.ws10_avg == -5555, meteo.ws10_avg, meteo.ws10_std)

    # Conversion types
    conversion = {'id': 'first', 'year': 'first', 'jday': 'first', 'min': 'first',
                  'temp_sfc': 'first', 'humid': 'first', 'press': 'first',
                  'prec': 'sum', 'ws10_avg': 'mean', 'wd10_avg': 'median', 'wd10_std': 'std', 'ws10_std': 'first'}

    # Mask to not resample this values
    Maska = meteo[(meteo != 3333.0) & (meteo != -5555) & (meteo != np.nan)]
    # Calculate standard deviation based resample
    Maska['ws10_std'] = Maska['ws10_avg'].resample("10min").agg(np.std)

    # Apply ressample based conversion
    Maska = Maska.resample('10min').agg(conversion)

    # Final DataFrame
    meteorological = Maska.fillna(meteo)
    # Reset index
    meteorological = meteorological.reset_index()
    
    ## Drop timestamp
    meteorological = meteorological.drop(columns='timestamp')

    # Get multiindex    
    mult_idx = multi_index(meteorological.columns)
    
    ## Sensor type
    sensor = ['','','','','tmo_aspira','hgr_aspira','bar_atmosf','plv_tipbuk','anm_sonico','anm_sonico','anm_sonico','anm_sonico','anm_sonico']

    ## Agregate sensor
    aux_idx = []
    for i in range(len(mult_idx)):
        aux_idx.append((mult_idx[i][0],mult_idx[i][1],sensor[i]))

    ## Add multindex
    mux = pd.MultiIndex.from_tuples(aux_idx)
    meteorological.columns = mux


    #### METEOROLOGICAL
    # Copy dataframe to drop columns
    solar = df.copy()
    ## Drop meteorological variables
    solar.drop(['Temp_sfc', 'Humid', 'Press', 'Prec', 'Ws10_AVG',
                'Wd10_AVG', 'Wd10_STD', 'CosAngZen'], axis=1, inplace=True)
        
    solar = solar.rename(columns=str.lower)
    solar = solar.rename(columns={id_: 'id'})


    columns1 = ['id','year','jday','min','glo_avg','glo_std','glo_max','glo_min','dif_avg','dif_std','dif_max','dif_min','par_avg','par_std','par_max','par_min','lux_avg','lux_std','lux_max','lux_min','dir_avg','dir_std','dir_max','dir_min','lw_avg','lw_std','lw_max','lw_min','temp_glo','temp_dir','temp_dif','temp_dome','temp_case']
    columns2 = ['','','','','W/m2','W/m2','W/m2','W/m2','W/m2','W/m2','W/m2','W/m2','µmols/m2.s','µmols/m2.s','µmols/m2.s','µmols/m2.s','klux','klux','klux','klux','W/m2','W/m2','W/m2','W/m2','W/m2','W/m2','W/m2','W/m2','°C','°C','°C','°C','°C']
    columns3 = ['','','','','pir_termpil','pir_termpil','pir_termpil','pir_termpil','pir_rastsbr','pir_rastsbr','pir_rastsbr','pir_rastsbr','par_fotodio','par_fotodio','par_fotodio','par_fotodio','lux_fotodio','lux_fotodio','lux_fotodio','lux_fotodio','phl_termpil','phl_termpil','phl_termpil','phl_termpil','prg_rastsbr','prg_rastsbr','prg_rastsbr','prg_rastsbr','tmo_ventil','tmo_ventil','tmo_ventil','tmo_ventil','tmo_ventil']
    
    columns = []
    
    for i in range(len(columns1)):
        columns.append((columns1[i],columns2[i],columns3[i]))
        

    mux = pd.MultiIndex.from_tuples(columns)
  
    solar.columns = mux
    
    return meteorological,solar
    
