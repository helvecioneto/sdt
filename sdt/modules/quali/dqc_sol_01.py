import pvlib as pvl
import numpy as np

def sol_dqc_01(dframe_,dict_):

    ### COPIA DO REAL
    dqc_ = dframe_.copy()
    dqc_.columns = dqc_.columns.droplevel(1)


    
    ## Le dicionario
    try:
        station = dframe_.acronym.unique()[0]
        id_ = int(dict_.loc[dict_['Sigla'] == station]['Id'].values[0])
        lat_ = dict_.loc[dict_['Sigla'] == station]['Latitude'].values[0]
        lon_ = dict_.loc[dict_['Sigla'] == station]['Longitude'].values[0]
        alt_ = dict_.loc[dict_['Sigla'] == station]['Altitude'].values[0]
    except:
        print('Station or ID not set on Dictionary!!! -> ',station)

    ## FOR LINE IN DQC_
    for i,row in dqc_.iterrows():

        ### Constante solar ajustada para distância Terra-Sol
        sa = pvl.irradiance.get_extra_radiation(datetime_or_doy=row.timestamp, solar_constant=1366.1, method='spencer')

        ### Ângulo do zênite solar
        AZS = pvl.solarposition.spa_python(time=row.timestamp,latitude=lat_,longitude=lon_,altitude=alt_)['zenith'].values[0]

        ## Nas fórmulas, se AZS > 90º u0 é considerado 0
        if AZS > 90:
            u0 = 0
        else:
            u0 = np.cos(np.radians(AZS))

        ### VARIAVEIS = ac
        ## GLOBAL HORIZONTAL
        ac = 'glo_avg'
        ### desvio padrão ≠ 0 (zero)
        if row[ac[:-3]+'std'] != 0:
            ### ANALISANDO VALOR
            value_to_analize = row[ac]
            
            ## FLAG VERIFICATION
            if value_to_analize == -5555 or value_to_analize == 3333:
                dqc_.loc[i,ac] = '5555'
                del value_to_analize,ac
            
            else:
                ### mín.: -4
                ### máx.: Sa × 1,5 × µ0^1,2 + 100
                min_v = - 4
                max_v = float(sa) * 1.5 * (float(u0) ** (1.2)) + 100

                ## APROVADO LEVEL 01
                if value_to_analize >= min_v and value_to_analize <= max_v:
                    # print('APROVADO!')
                    # print('Hora->',row.timestamp.strftime('%Y/%m/%d %H:%M'),' Glob->',np.round(value_to_analize,3),
                    #       ' min-> ',min_v,' max->',np.round(max_v,3),
                    #       ' sa->',np.round(sa,3),' u0->',np.round(u0,3))
                    
                    ## APROVADO LEVEL 01
                    dqc_.loc[i,ac] = '0009'
                    del min_v,max_v

                    ## CHECK LEVEL 02
                    min_v = - 2
                    max_v = float(sa) * 1.2 * (float(u0) ** (1.2)) + 50
                    if value_to_analize >= min_v and value_to_analize <= max_v:
                        ## APROVADO LEVEL 02
                        dqc_.loc[i,ac] = '0099'
                        del min_v,max_v,value_to_analize,ac
                    else:
                        ## REPROVADO LEVEL 02
                        dqc_.loc[i,ac] = '0029'
                        del min_v,max_v

                ## REPROVADO LEVEL 01
                else:
                    # print('REPROVADO!!!')
                    # print('Hora->',row.timestamp.strftime('%Y/%m/%d %H:%M'),' Glob->',np.round(value_to_analize,3),
                    #       ' min-> ',min_v,' max->',np.round(max_v,3),
                    #       ' sa->',np.round(sa,3),' u0->',np.round(u0,3))
                    
                    ## REPROVADO LEVEL 01
                    dqc_.loc[i,ac] = '5552'
                    del min_v,max_v,value_to_analize,ac

        else:
            ## REPROVADO DESVIO PADRAO
            dqc_.loc[i,ac] = '5552'
            del ac


    return dqc_,dframe_
