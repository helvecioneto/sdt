from dependecies import *
from modules.load_config import load_config

def met_dqc_03(dframe,dqc_df,past_path):
    
    ## TODQC
    dqc_df02 = dqc_df.copy()
    ## ORIG
    dframe_ = dframe.copy()
    ## Colunas analisadas
    analyze_columns = dframe.columns[5:]
    
    one_hour_obs = 72
    thre_hour_obs = 108
    
    ### Abrir arquivo passado
    try:
        past_frame = loadFile(past_path).tail(thre_hour_obs)
        past_frame.columns = past_frame.columns.droplevel(1)
        past_frame = past_frame.reset_index()
        past_frame = past_frame.drop(columns=['index'])
        
    except:
        past_frame = pd.DataFrame()

    ## Verifica se arquivo passado existe e adiciona incrmentos
    incremento01 = False
    if len(past_frame) > 0:
        incremento01 = True
        ## INCREMENTA LINHAS
        dframe_ = pd.concat([past_frame.tail(one_hour_obs),dframe_],axis=0,ignore_index=True)
        ### Create interval
        null_df = pd.DataFrame(columns=dqc_df.columns)
        for i in range(one_hour_obs):
            null_df.loc[i,:] = np.nan
        dqc_df = pd.concat([null_df.tail(one_hour_obs),dqc_df],axis=0,ignore_index=True)
    
    
    #### INTERVALO 12 HORA
    for ac in analyze_columns:
        ## Qualificar temperatura
        if 'tp_sfc' in ac:
            for i in range(one_hour_obs,len(dframe_)):
                ### Pega o valor na linha i
                analyze_value = dframe_.iloc[i][ac]
                ## Verifica se impossivel de qualificar
                if dqc_df.loc[i][ac].all() == '0552' or dqc_df.loc[i][ac].all() == '0005' or dqc_df.loc[i][ac].all() == '0052' or dqc_df.loc[i][ac].all() == '0059' or dqc_df.loc[i][ac].all() == '0029':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('REPROVADO!')
                    print('')
                    print('DQC FRAME')
                    print(dqc_df.loc[i][['timestamp',ac]].to_string())
                    print('')
                    print('DATA FRAME')
                    print(dframe_.loc[i][['timestamp',ac]].to_string())
                    input()
                    continue
                ## Verifica se linha é different das FLAGS
                if analyze_value != -5555 and analyze_value != 3333:
                    ## Array para extração
                    analyzed_array = dframe_.iloc[i-one_hour_obs:i][ac]
                    ## Valores diferrentes das flags
                    analyzed_array = analyzed_array[(analyzed_array != -5555) & (analyzed_array != 3333)]

                    ## Se os valores analizados forem maior que 2
                    if len(analyzed_array) >= 2:
                        array_max = np.nanmax(analyzed_array)
                        array_min = np.nanmin(analyzed_array)
                        variation = array_max - array_min
                        ## variação > 0.5° num período de 1 hora
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print('DEBUG')
                        print('Variavel -> ',ac)
                        print('')
                        print('Frame atual->\n',dframe_.iloc[i][['timestamp',ac]].to_string())
                        print('')
                        print('Frame passado ->\n',dframe_.iloc[i-one_hour_obs:i][['timestamp',ac]].to_string())
                        print('')
                        print('Valor analisado ->',analyze_value)
                        print('Valores passados -> ',analyzed_array.to_numpy())
                        print('')
                        if variation > 0.5:
                            ### dado de boa qualidade ou não suspeito
                            copy_dqc = dqc_df.loc[i][ac].values.tolist()
                            dqc_ok = copy_dqc[0][0:1] + '9' + copy_dqc[0][-2:]
                            dqc_df.loc[i,ac] = dqc_ok
                            print('Max ->',array_max)
                            print('Min ->',array_min)
                            print('Variação ->',variation)
                            print('')
                            print('DQC da linha ->',copy_dqc)
                            print('DQC adicionado -> ',dqc_ok)
                            input()
                        else:
                            ### dado suspeito de ser incorreto
                            copy_dqc = dqc_df.loc[i][ac].values.tolist()
                            dqc_no = copy_dqc[0][0:1] + '2' + copy_dqc[0][-2:]
                            dqc_df.loc[i,ac] = dqc_no
                            print('Variação ->',variation)
                            print('')
                            print('DQC da linha ->',copy_dqc)
                            print('DQC adicionado -> ',dqc_no)
                            input()
                    else:
                        ### procedimento não pode ser executado
                        copy_dqc = dqc_df.loc[i][ac].values.tolist()
                        dqc_none = copy_dqc[0][0:1] + '5' + copy_dqc[0][-2:]
                        dqc_df.loc[i,ac] = dqc_none
                        print('Variação ->',variation)
                        print('')
                        print('DQC da linha ->',copy_dqc)
                        print('DQC adicionado -> ',dqc_none)
                        input()
                else:
                    ### procedimento não pode ser executado
                    copy_dqc = dqc_df.loc[i][ac].values.tolist()
                    dqc_null = copy_dqc[0][0:1] + '0' + copy_dqc[0][-2:]
                    dqc_df.loc[i,ac] = dqc_null
                    print('Variação ->',variation)
                    print('')
                    print('DQC da linha ->',copy_dqc)
                    print('DQC adicionado -> ',dqc_null)
                    input()
                    
        ## Qualificar direcao vento
        if 'wd10_avg' in ac:
            for i in range(thre_hour_obs,len(dframe_)):
                ### Pega o valor na linha i
                analyze_value = dframe_.iloc[i][ac]
                ## Verifica se impossivel de qualificar
                if dqc_df.loc[i][ac].all() == '0552' or dqc_df.loc[i][ac].all() == '0005' or dqc_df.loc[i][ac].all() == '0052' or dqc_df.loc[i][ac].all() == '0059':
                    continue

                ## Verifica se linha é different das FLAGS
                if analyze_value != -5555 and analyze_value != 3333:
                    ## Array para extração
                    analyzed_array = dframe_.iloc[i-6:i][ac]
                    ## Valores diferrentes das flags
                    analyzed_array = analyzed_array[(analyzed_array != -5555) & (analyzed_array != 3333)]
                    ## Se os valores analizados forem maior que 2
                    if len(analyzed_array) >= 2:
                        mx = np.nanmax(analyzed_array)
                        mi = np.nanmin(analyzed_array)
                        if mx - mi > 180:
                            ab = abs((mx - mi) - 360)
                        else:
                            ab = abs(mx - mi)
                        if ab > 10:
                            ### dado de boa qualidade ou não suspeito
                            copy_dqc = dqc_df.loc[i][ac].values.tolist()
                            dqc_ok = copy_dqc[0][0:1] + '9' + copy_dqc[0][-2:]
                            dqc_df.loc[i,ac] = dqc_ok
                        else:
                            ## dado suspeito de ser incorreto
                            copy_dqc = dqc_df.loc[i][ac].values.tolist()
                            dqc_no = copy_dqc[0][0:1] + '2' + copy_dqc[0][-2:]
                            dqc_df.loc[i,ac] = dqc_no
                    else:
                        ### procedimento não pode ser executado
                        copy_dqc = dqc_df.loc[i][ac].values.tolist()
                        dqc_none = copy_dqc[0][0:1] + '5' + copy_dqc[0][-2:]
                        dqc_df.loc[i,ac] = dqc_none
                else:
                    ### nenhum procedimento foi executado
                    copy_dqc = dqc_df.loc[i][ac].values.tolist()
                    dqc_null = copy_dqc[0][0:1] + '0' + copy_dqc[0][-2:]
                    
    ### REMOVE NAN e INCREMENTAL
    dqc_df = dqc_df.dropna()
    if incremento01 == True:
        dframe_ =  dframe_.iloc[one_hour_obs:]
        
    ### Intervalo 18 HORAS
    ## Verifica se arquivo passado existe e adiciona incrmentos
    incremento02 = False
    if len(past_frame) > 0:
        incremento02 = True
        ## INCREMENTA LINHAS
        dframe_ = pd.concat([past_frame.tail(thre_hour_obs),dframe_],axis=0,ignore_index=True)
        ### Create interval
        null_df = pd.DataFrame(columns=dqc_df.columns)
        for i in range(thre_hour_obs):
            null_df.loc[i,:] = np.nan
        dqc_df = pd.concat([null_df.tail(thre_hour_obs),dqc_df],axis=0,ignore_index=True)
    
    #### INTERVALO 1 HORA
    for ac in analyze_columns:                  
        ## Qualificar vento velocidade
        if 'ws10_avg' in ac:
            for i in range(thre_hour_obs,len(dframe_)):
                ### Pega o valor na linha i
                analyze_value = dframe_.iloc[i][ac]
                ## Verifica se impossivel de qualificar
                if dqc_df.loc[i][ac].all() == '0552' or dqc_df.loc[i][ac].all() == '0005' or dqc_df.loc[i][ac].all() == '0052' or dqc_df.loc[i][ac].all() == '0059':
                    continue
                ## Verifica se linha é different das FLAGS
                if analyze_value != -5555 and analyze_value != 3333:
                    ## Array para extração
                    analyzed_array = dframe_.iloc[i-thre_hour_obs:i][ac]
                    ## Valores diferrentes das flags
                    analyzed_array = analyzed_array[(analyzed_array != -5555) & (analyzed_array != 3333)]
                    ## Se os valores analizados forem maior que 2
                    if len(analyzed_array) >= 2:
                        array_max = np.nanmax(analyzed_array)
                        array_min = np.nanmin(analyzed_array)
                        variation = array_max - array_min
                        ## variação > 0,1 num período de 3 horas consecutivas
                        if variation > 0.1:
                            ### dado de boa qualidade ou não suspeito
                            copy_dqc = dqc_df.loc[i][ac].values.tolist()
                            dqc_ok = copy_dqc[0][0:1] + '9' + copy_dqc[0][-2:]
                            dqc_df.loc[i,ac] = dqc_ok
                        else:
                            ### dado suspeito de ser incorreto
                            copy_dqc = dqc_df.loc[i][ac].values.tolist()
                            dqc_no = copy_dqc[0][0:1] + '2' + copy_dqc[0][-2:]
                            dqc_df.loc[i,ac] = dqc_no
                    else:
                        ### procedimento não pode ser executado
                        copy_dqc = dqc_df.loc[i][ac].values.tolist()
                        dqc_none = copy_dqc[0][0:1] + '5' + copy_dqc[0][-2:]
                        dqc_df.loc[i,ac] = dqc_none
                else:
                    ### nenhum procedimento foi executado
                    copy_dqc = dqc_df.loc[i][ac].values.tolist()
                    dqc_null = copy_dqc[0][0:1] + '0' + copy_dqc[0][-2:]
                  
    ### REMOVE NAN e INCREMENTAL
    dqc_df = dqc_df.dropna()
    if incremento02 == True:
        dframe_ =  dframe_.iloc[thre_hour_obs:]
    
    ## REINDEX
    dqc_df = dqc_df.reset_index()
    dqc_df = dqc_df.drop(columns=['index'])
    
    return dqc_df

def loadFile(path):
    df = pd.read_csv(path, header=[0, 1])
    cols = []
    for c in df.columns:
        if 'Unnamed' in c[1]:
            c_ = ''
        else:
            c_ = c[1]
        cols.append((c[0],c_))
    mux = pd.MultiIndex.from_tuples(cols)
    df.columns = mux
    ## Transforma coluna temporal
    df['timestamp'] = pd.to_datetime(df.timestamp, format='%Y-%m-%d %H:%M:%S')
    return df
