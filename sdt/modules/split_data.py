# -*- coding: utf-8 -*-
from modules.load_stations import load_stations
from modules.load_config import load_config
from modules.top_header import top_header

from dependecies import *
warnings.filterwarnings('ignore')

## Global variables
config = load_config()

## Debug dir
debug_dir = config[0]['DEBUG_DIR']

## Used to copy header
aux = config[0]['MET_HEADER'].copy()
aux2 = config[0]['SOLAR_HEADER'].copy()

meteoH = config[0]['meteoH']
solarH = config[0]['solarH']
BRUTE_HEADER = config[0]['BRUTE_HEADER']
MET_HEADER = config[0]['MET_HEADER']
SOLAR_HEADER = config[0]['SOLAR_HEADER']

try:
    MET_UPDATE = config[0]['MET_UPDATE']
    SOL_UPDATE = config[0]['SOL_UPDATE']
except:
    MET_UPDATE = None
    SOL_UPDATE = None


def split_data():

    top_header('Main Menu > Solarimetric > Split Data')
    print('\t\tPlease select an option\n')
    
    files = load_stations()
    process_files(files)
    
def process_files(files):
    
    debug_di = str(debug_dir) + 'split_warning_logs.txt'
    logging.basicConfig(filename=debug_di, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logger.setLevel(logging.INFO)
    
    for file in sorted(files):
        try:
            df = pd.read_table(file,header=None, sep=',')
            df.columns = BRUTE_HEADER
        except:
            logging.warning('Error to read at file: '+str(file)+'')
            print('Error in Meteorological variables: ', file)
            
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            process_meteo(df[meteoH].rename(columns=str.lower),file)
        except:
            logging.warning('Error in Meteorological variables at file: '+str(file)+'')
            print('Error in Meteorological variables: ', file)
        try:
            process_solar(df[solarH].rename(columns=str.lower),file)
        except:
            logging.warning('Error in Solarimetric variables at file: '+str(file)+'')
            print('Error in Solarimetric variables: ', file)
        ## Continue
        input("Press Enter to Continue:")
        ## Clean screan and print first 20 
        os.system('cls' if os.name == 'nt' else 'clear')
    print("All files are translated!!")
    

def process_meteo(meteo,file):
    config = load_config()
    meteo['timestamp'] = pd.to_datetime(meteo.year, format='%Y') + pd.to_timedelta(meteo.day - 1, unit='d')  + pd.to_timedelta(meteo['min'], unit='m')
    meteo = meteo.set_index('timestamp')
    
    ##for calc ws10_std
    meteo['ws10_std'] = meteo['ws10_avg']
    
    ## Rename columns
    meteo.rename(columns={'day':'jday','temp_sfc':'tp_sfc','prec':'rain'},inplace=True)

    # Converstions    
    conversion = {'id': 'first', 'year': 'first', 'jday': 'first', 'min': 'first',
                  'tp_sfc': 'first', 'humid': 'first', 'press': 'first','rain': 'sum',
                  'ws10_avg': 'mean','ws10_std': 'std', 'wd10_avg': lambda x: arctan(x.values), 'wd10_std': lambda x: yamartino(x.values)}
    
    #Mask to not resample incorrect values
    Maska = meteo[(meteo != 3333.0) & (meteo != -5555) & (meteo != np.nan)]
    
     #Apply ressample based conversion
    Maska = Maska.resample('10min').agg(conversion)
    
    
    # frame.resample('1H').agg({'radiation': np.sum, 'tamb': np.mean})
    
    ## Unmask values
    Unmask = meteo[(meteo == 3333.0)].resample('10min').first()
    Unmask2 = meteo[(meteo == -5555)].resample('10min').first()
    
    ## Combine values
    meteorological = Unmask.combine_first(Maska)
    meteorological = Unmask2.combine_first(meteorological)
    
    ## Reset index
    meteorological = meteorological.reset_index()
    # Realocate order of columns
    meteorological = meteorological.reindex(columns=['id','timestamp','year','jday','min',
                                                     'tp_sfc','humid','press','rain',
                                                     'ws10_avg','ws10_std','wd10_avg','wd10_std'])
            
    ## Change type of columns
    meteorological[['id','year','jday','min']] = meteorological[['id','year','jday','min']].astype(int)

    ## Header check
    year_ = file.parent.name
    ## Extract month string
    month = (meteorological['timestamp'][0].strftime('%m'))
    stat_ = file.parent.parent.name 
    output = config[0]['FORMATED_OUT']+stat_+'/Meteorologicos/'+year_+'/'+stat_+'_'+year_+'_'+month+'_MD_formatado.csv'
              
        ### Create dir of output if not exist
    if not os.path.exists(os.path.dirname(output)):
        try:
            os.makedirs(os.path.dirname(output))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    ## Update Global MET_HEADER
    global MET_HEADER
    # For key in MET_UPDATE Check    
    met1 = []
    met2 = []


    ##Change ID by name of station
    meteorological['id'] = stat_

    # Create Multindex based in columns from header_log
    mux = pd.MultiIndex.from_tuples(MET_HEADER)
            # Fix multindex on dataframe
    meteorological.columns = mux
    
    #Aux out
    out_met = []

    if MET_UPDATE != None:
        for k in MET_UPDATE:
            ## Check if Updat is the station
            if (k[0][0] == stat_):
                if len(meteorological.loc[meteorological['timestamp'] >= k[1]]) > 0:
                    for kk in k:
                        # Update Global variable
                        for idx, item in enumerate(MET_HEADER):
                            if kk[0] in  item[0]:
                                MET_HEADER[idx] = kk
    
                    # Separete files
                    met1 = meteorological.loc[meteorological['timestamp'] >= k[1]]
                    # Create Multindex based in columns from header_log
                    mux1 = pd.MultiIndex.from_tuples(MET_HEADER)
                    # Fix multindex on dataframe
                    met1.columns = mux1
                    
                    ## Second file
                    met2 = meteorological.loc[meteorological['timestamp'] < k[1]]
                    mux2 = pd.MultiIndex.from_tuples(aux)
                    met2.columns = mux2
                    
                    if len(met1) > len(met2):
                        # Rename
                        met2.columns = mux1
                        # Concat
                        out_met = [met1,met2]
                        out_met = pd.concat(out_met)
                        # Sort
                        out_met = out_met.sort_values(by=['timestamp'])
                    else:
                        #Rename
                        met2.columns = mux2
                        # Concat
                        out_met = [met2,met1]
                        out_met = pd.concat(out_met)
                        # Sort
                        out_met = out_met.sort_values(by=['timestamp'])
 
    # If equals
    if (meteorological.equals(out_met)):
        # Clean screan and print first 20 
        print('Processing File -> ',file)
        print('\nSplit weather data!: ')
        ## Drop second line of multindex
        meteorological.columns = meteorological.columns.droplevel(1)
        print(meteorological)
        meteorological.to_csv(output,index=False)
        
    # If diference
    elif (len(out_met)) > 0:
        # Clean screan and print first 20 
        ## Save files
        print('\nSplit weather data!: ',output)
        ## Drop second line of multindex
        out_met.columns = out_met.columns.droplevel(1)
        print(out_met,'\n')
        
        out_met.to_csv(output,index=False)
    else:
        # Clean screan and print first 20 
        print('Processing File -> ',file)
        print('\nSplit weather data!: ',output)
        ## Drop second line of multindex
        meteorological.columns = meteorological.columns.droplevel(1)
        print(meteorological)
        
        meteorological.to_csv(output,index=False)

# Yamartin mean
# Yamartin mean
def yamartino(thetalist):
    s=0
    c=0
    n=0.0
    for theta in thetalist:
        s=s+sin(radians(theta))
        c=c+cos(radians(theta))
        n+=1
    s=s/n
    c=c/n
    try:
        eps=(1-(s**2+c**2))**0.5
        sigma=asin(eps)*(1+(2.0/3.0**0.5-1)*eps**3)
        return degrees(sigma)
    except:
        return -9999

## Calc arctan
def arctan(thetalist):
    s=0
    c=0
    n=0.0
    for theta in thetalist:
        s=s+sin(radians(theta))
        c=c+cos(radians(theta))
        n+=1
    s=s/n
    c=c/n
    ## Calc arctan
    arctan = np.arctan(s/c)
    ## Convert rad to degress
    arctan = degrees(arctan)
    # Check arctan negative values
    if arctan < 0:
        arctan = arctan + 360
    
    return arctan

def process_solar(solar,file):

    config = load_config()
    ## Create Timestamp    
    solar['timestamp'] = pd.to_datetime(solar.year, format='%Y') + pd.to_timedelta(solar.day - 1, unit='d')  + pd.to_timedelta(solar['min'], unit='m')

    # Change position of timestamp    
    cols = list(solar)
    cols.insert(1, cols.pop(cols.index('timestamp')))
    solar = solar.loc[:, cols]
    
    ## Header check
    year_ = file.parent.name
    month = (solar['timestamp'][0].strftime('%m'))
    stat_ = file.parent.parent.name
    output = config[0]['FORMATED_OUT']+stat_+'/Solarimetricos/'+year_+'/'+stat_+'_'+year_+'_'+month+'_SD_formatado.csv'
    
    ### Create dir of output if not exist
    if not os.path.exists(os.path.dirname(output)):
        try:
            os.makedirs(os.path.dirname(output))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
                
    ## Update Global SOLAR_HEADER
    global SOL_UPDATE
    # For key in SOLAR_UPDATE Check    
    sol1 = []
    sol2 = []
    
    ##Change ID by name of station
    solar['id'] = stat_
    
    # Create Multindex based in columns from header_log
    mux = pd.MultiIndex.from_tuples(SOLAR_HEADER)
            # Fix multindex on dataframe
    solar.columns = mux
    
    # Aux
    out_sol = []

    if SOL_UPDATE != None:
        for k in SOL_UPDATE:
            ## Check if Updat is the station
            if (k[0][0] == stat_):
                if len(solar.loc[solar['timestamp'] >= k[1]]) > 0:
                    for kk in k:
                        # Update Global variable
                        for idx, item in enumerate(SOLAR_HEADER):
                            if kk[0] in  item[0]:
                                SOLAR_HEADER[idx] = kk
    
                    # Separete files
                    sol1 = solar.loc[solar['timestamp'] >= k[1]]
                    # Create Multindex based in columns from header_log
                    mux1 = pd.MultiIndex.from_tuples(SOLAR_HEADER)
                    # Fix multindex on dataframe
                    sol1.columns = mux1
                    
                    ## Second file
                    sol2 = solar.loc[solar['timestamp'] < k[1]]
                    mux2 = pd.MultiIndex.from_tuples(aux2)
                    sol2.columns = mux2
                    
                    if len(sol1) > len(sol2):
                        # Rename
                        sol2.columns = mux1
                        # Concat
                        out_sol = [sol1,sol2]
                        out_sol = pd.concat(out_sol)
                        # Sort
                        out_sol = out_sol.sort_values(by=['timestamp'])
                    else:
                        #Rename
                        sol2.columns = mux2
                        # Concat
                        out_sol = [sol2,sol1]
                        out_sol = pd.concat(out_sol)
                        # Sort
                        out_sol = out_sol.sort_values(by=['timestamp'])                
            
                         
    if (solar.equals(out_sol)):
        # Clean screan and print first 20 
        print('Processing File -> ',file)
        print('\nSplit weather data!: ')
        # Drop second level of multindex
        solar.columns = solar.columns.droplevel(1)
        print(solar)
        solar.to_csv(output,index=False)
    elif (len(out_sol)) > 0:
        # Clean screan and print first 20 
        ## Save files
        print('\nSplit weather data!: ',output)
        # Drop second level of multindex
        out_sol.columns = out_sol.columns.droplevel(1)
        print(out_sol)
        out_sol.to_csv(output,index=False)
    else:
        # Clean screan and print first 20 
        print('Processing File -> ',file)
        print('\nSplit weather data!: ',output)
        # Drop second level of multindex
        solar.columns = solar.columns.droplevel(1)
        print(solar)
        solar.to_csv(output,index=False)
