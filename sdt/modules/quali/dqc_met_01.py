from dependecies import *
from modules.load_config import load_config
from modules.quali.config import temp_min,temp_max,press_max,press_min,rain_max

def met_dqc_01(dframe_,dict_):
    
    ### COPIA DO REAL
    dframe_copy = dframe_.copy()
    dframe_copy.columns = dframe_copy.columns.droplevel(1)

    ## Convert multindex
    cols = []
    for c in dframe_.columns:
        if c[1] != '':
            c_ = 'dqc_v1'
            cols.append((c[0],c_))
        else:
            cols.append((c[0],''))
    mux = pd.MultiIndex.from_tuples(cols)
    dframe_.columns = mux
    
    ## Le dicionario
    try:
        station = dframe_.acronym.unique()[0]
        id_ = int(dict_.loc[dict_['Sigla'] == station]['Id'].values[0])
        month_ = str(dframe_copy['timestamp'].dt.strftime('%m').unique()[0])
    except:
        print('Station or ID not set on Dictionary!!! -> ',station)

    ## Sazonal variables
    l_temps_max = temp_max.loc[temp_max['id'] == id_]
    l_temps_min = temp_min.loc[temp_min['id'] == id_]
    l_rain_max = rain_max.loc[rain_max['id'] == id_]
    
    max_temp = l_temps_max[month_].values[0]
    min_temp = l_temps_min[month_].values[0]
    max_rain = l_rain_max[month_].values[0]

    ## Non Sazonal
    max_press = press_max.loc[press_max['id'] == id_]['max'].values[0]
    min_press = press_min.loc[press_min['id'] == id_]['min'].values[0]

    ## Colunas analisadas
    analyze_columns = dframe_copy.columns[5:]
    
    ### Pegar indices
    for ac in analyze_columns:
        ## Qualificar temperatura
        if 'tp_sfc' in ac:
            DQC_OK,DQC_NO,DQC_NULL = operation(dframe_copy,ac,min_temp,max_temp)
            ## QUALIFY
            dframe_.loc[DQC_OK,ac] = '0009'
            dframe_.loc[DQC_NO,ac] = '0552'
## DESSE JEITO CERRTO NULL OLHAR NOS DQC_MET 2 e 3
            dframe_.loc[DQC_NULL,ac] = '0555'
        ## Qualificar humidade
        if 'humid_sfc' in ac:
            DQC_OK,DQC_NO,DQC_NULL = operation(dframe_copy,ac,0,100)
            ## QUALIFY
            dframe_.loc[DQC_OK,ac] = '0009'
            dframe_.loc[DQC_NO,ac] = '0002'     
            dframe_.loc[DQC_NULL,ac] = '0005'
        ## Qualificar pressão
        if 'press' in ac:
            DQC_OK,DQC_NO,DQC_NULL = operation(dframe_copy,ac,min_press,max_press)
            ## QUALIFY
            dframe_.loc[DQC_OK,ac] = '0009'
            dframe_.loc[DQC_NO,ac] = '0052'
            dframe_.loc[DQC_NULL,ac] = '0055'
        ## Qualificar rain
        if 'rain' in ac:
            DQC_OK,DQC_NO,DQC_NULL = operation(dframe_copy,ac,0,max_rain)
            ## QUALIFY
            dframe_.loc[DQC_OK,ac] = '0009'
            dframe_.loc[DQC_NO,ac] = '0052'
            dframe_.loc[DQC_NULL,ac] = '0055'
        ## Qualificar vento velocidade
        if 'ws10_avg' in ac:
            DQC_OK,DQC_NO,DQC_NULL = operation(dframe_copy,ac,0,25)
            ## QUALIFY
            dframe_.loc[DQC_OK,ac] = '0009'
            dframe_.loc[DQC_NO,ac] = '5552'
            dframe_.loc[DQC_NULL,ac] = '5555'
        ## Qualificar vento direcao
        if 'wd10_avg' in ac:
            DQC_OK,DQC_NO,DQC_NULL = operation(dframe_copy,ac,0,360)
            ## QUALIFY
            dframe_.loc[DQC_OK,ac] = '0009'
            dframe_.loc[DQC_NO,ac] = '0552'
            dframe_.loc[DQC_NULL,ac] = '0555'
    return dframe_,dframe_copy

def operation(dframe_ana,var,opMin,opMax):
    ## FLAGS
    FLAG01 = -5555
    FLAG02 = 3333
    ## Index different flags
    ana_idx = dframe_ana.loc[(dframe_ana[var] != FLAG01) & (dframe_ana[var] != FLAG02)].index
    non_idx = dframe_ana.loc[(dframe_ana[var] == FLAG01) | (dframe_ana[var] == FLAG02)].index
    ana_df = dframe_ana.loc[ana_idx][var]
    DQC_OK = ana_df[(ana_df >= opMin) & (ana_df <= opMax)].index
    DQC_NO = ana_df.index.difference(DQC_OK)
    DQC_NULL = non_idx
    return DQC_OK,DQC_NO,DQC_NULL
