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

    ## FOR LINE IN DATAFRAME
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

        ### Global Horizontal (Wm²)
        glob_avg_dqc = glo_avg_validation(value=row['glo_avg'],value_std=row['glo_std'],dif=row['dif_avg'],ghi=row['glo_avg'],sa_=sa,u0_=u0,azs_=AZS)

        ### Direta Normal (Wm²)
        dir_avg_dqc = dir_avg_validation(value=row['dir_avg'],value_std=row['dir_std'],dni=row['dir_avg'],ghi=row['glo_avg'],dif=row['dif_avg'],sa_=sa,u0_=u0,azs_=AZS)

        ### Difusa (Wm²)
        dif_avg_dqc = dif_avg_validation(value=row['dif_avg'],value_std=row['dif_std'],dif=row['dif_avg'],ghi=row['glo_avg'],sa_=sa,u0_=u0,azs_=AZS)

        ### Onda Longa (Wm²)
        lw_avg_dqc = lw_avg_validation(value=row['lw_avg'],value_std=row['lw_std'])

        ### PAR (umols s-¹m-²)
        par_avg_dqc = par_avg_validation(value=row['par_avg'],value_std=row['par_std'],sa_=sa,u0_=u0)

        ### Iluminância (klux)
        lux_avg_dqc = par_avg_validation(value=row['lux_avg'],value_std=row['lux_std'],sa_=sa,u0_=u0)


        print(row['timestamp'],row['lux_avg'],lux_avg_dqc)


    return dqc_,dframe_


# Routine validation: Global Radiation (W/m²)
def glo_avg_validation(value,value_std,dif,ghi,sa_,u0_,azs_):

    # ### desvio padrão ≠ 0 (zero)
    # ## Por enquanto critério não aplicável devido a problemas no desvio padrão em arquivos antigos.
    # if value_std == 0:
    #     ## REPROVADO DESVIO PADRAO
    #     return '5552'

    ## FLAG VERIFICATION
    if value == -5555 or value == 3333:
        return '5555'

    # Start of the routine validation: Global Radiation (W/m²)
    else:
        ### mín.: -4
        ### máx.: Sa × 1,5 × µ0^1,2 + 100
        min_v = - 4
        max_v = float(sa_) * 1.5 * (float(u0_) ** (1.2)) + 100

        ## CHECK LEVEL 01
        if value >= min_v and value <= max_v:
            ## APROVADO LEVEL 01
            min_v2 = - 2
            max_v2 = float(sa_) * 1.2 * (float(u0_) ** (1.2)) + 50

            ## CHECK LEVEL 02
            if value >= min_v2 and value <= max_v2:

                ##CHECK LEVEL 03
                ## (Gueymard,2015)
                ## AZS < 75
                if ghi > 50 and azs_ < 75:
                    if (dif / ghi) < 1.05:
                        return '5999'
                    else:
                        return '5299'
                ## AZS > 75
                elif ghi > 50 and azs_ > 75:
                    if (dif / ghi) < 1.10:
                        return '5999'
                    else:
                        return '5299'

                ## LABREN
                elif ghi < 50:
                    if dif - ghi < 15:
                        return '5999'
                    else:
                        return '5299'

                ## REPROVADO LEVEL 03
                else:
                    return '5299'

            ## REPROVADO LEVEL 02
            else:
                return '5529'

        ## REPROVADO LEVEL 01
        else:
            return '5552'


# Routine validation: Direta Normal (W/m²)
def dir_avg_validation(value,value_std,dni,ghi,dif,sa_,u0_,azs_):

    # ### desvio padrão ≠ 0 (zero)
    # ## Por enquanto critério não aplicável devido a problemas no desvio padrão em arquivos antigos.
    # if value_std == 0:
    #     ## REPROVADO DESVIO PADRAO
    #     return '5552'

    ## FLAG VERIFICATION
    if value == -5555 or value == 3333:
        return '5555'

    # Start of the routine validation: Direta Normal (W/m²)
    else:
        ### mín.: -4
        ### máx.: Sa
        min_v = - 4
        max_v = float(sa_)

        ## CHECK LEVEL 01
        if value >= min_v and value <= max_v:
            ## APROVADO LEVEL 01
            min_v2 = - 2
            max_v2 = float(sa_) * 0.95 * (float(u0_) ** (0.2)) + 10

            ## CHECK LEVEL 02
            if value >= min_v2 and value <= max_v2:
                ##CHECK LEVEL 03

                ## CHECK LEVEL 03
                if (dni * u0_) - 50 <= ghi * (ghi - dif):
                    ## CHECAR ESSE DUPLO IF
                    if ghi * (ghi - dif) <= dni:
                        return '5999'
                    ## REPROVADO LEVEL 03
                    else:
                        return '5299' 
                ## REPROVADO LEVEL 03
                else:
                    return '5299' 

            ## REPROVADO LEVEL 02
            else:
                return '5529'
        ## REPROVADO LEVEL 01
        else:
            return '5552'

# Routine validation: Difusa (W/m²)
def dif_avg_validation(value,value_std,dif,ghi,sa_,u0_,azs_):

    # ### desvio padrão ≠ 0 (zero)
    # ## Por enquanto critério não aplicável devido a problemas no desvio padrão em arquivos antigos.
    # if value_std == 0:
    #     ## REPROVADO DESVIO PADRAO
    #     return '5552'

    ## FLAG VERIFICATION
    if value == -5555 or value == 3333:
        return '5555'

    # Start of the routine validation: Difusa (W/m²)
    else:
        min_v = - 4
        max_v = float(sa_) * 0.95 * (float(u0_) ** (1.2)) + 50

        ## CHECK LEVEL 01
        if value >= min_v and value <= max_v:

            ## APROVADO LEVEL 01
            min_v2 = - 2
            max_v2 = float(sa_) * 0.75 * (float(u0_) ** (1.2)) + 30

            ## CHECK LEVEL 02
            if value >= min_v2 and value <= max_v2:

                ##CHECK LEVEL 03
                ## AZS < 75
                if ghi > 50 and azs_ < 75:
                    if (dif / ghi) < 1.05:
                        return '5999'
                    else:
                        return '5299'
                ## AZS > 93
                elif ghi > 50 and azs_ > 93:
                    if (dif / ghi) < 1.10:
                        return '5999'
                    else:
                        return '5299'

                ## LABREN
                elif ghi > 50:
                        return '5999'

                ## REPROVADO LEVEL 03
                else:
                    return '5299'

            ## REPROVADO LEVEL 02
            else:
                return '5529'

        ## REPROVADO LEVEL 01
        else:
            return '5552'

def lw_avg_validation(value,value_std):
    # ### desvio padrão ≠ 0 (zero)
    # ## Por enquanto critério não aplicável devido a problemas no desvio padrão em arquivos antigos.
    # if value_std == 0:
    #     ## REPROVADO DESVIO PADRAO
    #     return '5552'

    ## FLAG VERIFICATION
    if value == -5555 or value == 3333:
        return '0555'

    # Start of the routine validation: Onda Longa (W/m²)
    else:
        min_v = 40
        max_v = 700

        ## CHECK LEVEL 01
        if value >= min_v and value <= max_v:

            ## APROVADO LEVEL 01
            min_v2 = 60
            max_v2 = 500

            ## CHECK LEVEL 02
            if value >= min_v2 and value <= max_v2:
                return '0599'

            ## REPROVADO LEVEL 02
            else:
                return '0529'

        ## REPROVADO LEVEL 01
        else:
            return '0552'


def par_avg_validation(value,value_std,sa_,u0_):
    # ### desvio padrão ≠ 0 (zero)
    # ## Por enquanto critério não aplicável devido a problemas no desvio padrão em arquivos antigos.
    # if value_std == 0:
    #     ## REPROVADO DESVIO PADRAO
    #     return '5552'

    ## FLAG VERIFICATION
    if value == -5555 or value == 3333:
        return '0555'

    # Start of the routine validation: PAR
    else:
        min_v = - 4
        max_v = 2.07 * (sa_ * 1.5 * (u0_**1.2) + 100)

        ## CHECK LEVEL 01
        if value >= min_v and value <= max_v:
            ## APROVADO LEVEL 01
            min_v2 = - 2
            max_v2 = 2.07 * (sa_ * 1.2 * (u0_**1.2) + 50)

            ## CHECK LEVEL 02
            if value >= min_v2 and value <= max_v2:
                return '0599'

            ## REPROVADO LEVEL 02
            else:
                return '0529'

        ## REPROVADO LEVEL 01
        else:
            return '0552'


def lux_avg_validation(value,value_std,sa_,u0_):
    # ### desvio padrão ≠ 0 (zero)
    # ## Por enquanto critério não aplicável devido a problemas no desvio padrão em arquivos antigos.
    # if value_std == 0:
    #     ## REPROVADO DESVIO PADRAO
    #     return '5552'

    ## FLAG VERIFICATION
    if value == -5555 or value == 3333:
        return '0555'

    # Start of the routine validation: PAR
    else:
        min_v = - 4
        max_v = 0.1125 * (sa_ * 1.5 * (u0_**1.2) + 100)

        ## CHECK LEVEL 01
        if value >= min_v and value <= max_v:
            ## APROVADO LEVEL 01
            min_v2 = - 2
            max_v2 = 0.1125 * (sa_ * 0.95 * (u0_**1.2) + 50)

            ## CHECK LEVEL 02
            if value >= min_v2 and value <= max_v2:
                return '0599'

            ## REPROVADO LEVEL 02
            else:
                return '0529'

        ## REPROVADO LEVEL 01
        else:
            return '0552'