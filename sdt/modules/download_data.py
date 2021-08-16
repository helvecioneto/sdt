# -*- coding: utf-8 -*-
  
from dependecies import *
from modules.load_config import load_config
from modules.top_header import top_header

config_file = load_config()

def download_stations():
    top_header('Main Menu > Preprocessing Mode > Download Data')
    stations,ftp_con = connection()
    ### Station
    count = -1
    for f in stations:
        count = count + 1
        print ("\t\t [%s]"  % count + f)
        
    while True:
        try:
            ans_file = int(input("\t\t Select Station: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_file > count:
            print ("\t\t Wrong selection.")
            continue
        files_dir = load_config()[0]['FTP_DIR'] + stations[ans_file] + '/data/'
        download_files(files_dir,ftp_con,stations[ans_file])
        break
    
def connection():
    stations_list = []
    try:
        print('\t\tConecting...')
        ftp = FTP(config_file[0]['FTP_IP'])
        ftp.login(config_file[0]['FTP_USER'],config_file[0]['FTP_PASS'])
        time.sleep(2)
        print('\t\tConnection established!')
        print('')
        print('\t\tPlease select one station')
        stations_list,ftp_con = get_station_list(ftp)
        
        return stations_list,ftp_con
         
    except:
        time.sleep(2)
        print('Connection failed')
        print('Enter to try again or press "Q" to Quit')
        choice = input()
        if choice=="Q" or choice=="q":
            sys.exit
        else:
            connection()
    
def get_station_list(ftp):
    
    ftp_dir = config_file[0]['FTP_DIR']
    
    ## Add STATIONS
    lt_stations = ['sms']
    
    # direc_st = []
    # for station in ftp.nlst(directory):
    #     if "." in station:
    #         pass
    #     else:
    #         lt_stations.append(station[-3:])
    #         direc_st.append(station)
    
    return lt_stations,ftp

def download_files(directory,connection,station):

    top_header('Main Menu > Preprocessing Mode > Download Data > '+str(station))
    print('\t\tPlease select type of the data to download: ')

    choice = input("""
                  0: All
                  1: Meteorological - MD
                  2: Solarimetric - SD
                  3: Anemometric - 10
                  4: Anemometric - 25
                  5: Anemometric - 50
                  B: Back
                  Q: Quit
                  Please enter your choice: """)

    if choice == "All" or choice =="0":
        pathlib.Path(config_file[0]['OPERATIONAL_IN']+str(station)).mkdir(parents=True, exist_ok=True)
        
        os.chdir(config_file[0]['OPERATIONAL_IN']+str(station))
        print(config_file[0]['OPERATIONAL_IN']+str(station))
        
        connection.cwd(directory)
        
        for filename in connection.nlst('*.DAT'):
            fhandle = open(filename, 'wb')
            print ('\t\tDownloading... ' + filename)
            connection.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        print('All files has been downloaded!')
        

        
    elif choice == "Meteorological" or choice =="1":
        pathlib.Path(config_file[0]['OPERATIONAL_IN']+'/'+str(station)).mkdir(parents=True, exist_ok=True)
        os.chdir(config_file[0]['OPERATIONAL_IN']+'/'+str(station))
        
        connection.cwd(directory)
        
        for filename in connection.nlst('*MD.DAT'):
            fhandle = open(filename, 'wb')
            print ('\t\tDownloading... ' + filename)
            connection.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        print('All files has been downloaded!')
        
    elif choice == "Solarimetric" or choice =="2":
        pathlib.Path(config_file[0]['OPERATIONAL_IN']+'/'+str(station)).mkdir(parents=True, exist_ok=True)
        os.chdir(config_file[0]['OPERATIONAL_IN']+'/'+str(station))
        
        connection.cwd(directory)
        
        for filename in connection.nlst('*SD.DAT'):
            fhandle = open(filename, 'wb')
            print ('\t\tDownloading... ' + filename)
            connection.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        print('All files has been downloaded!')
        
    elif choice == "Anemometric10" or choice =="3":
        pathlib.Path(config_file[0]['OPERATIONAL_IN']+'/'+str(station)).mkdir(parents=True, exist_ok=True)
        os.chdir(config_file[0]['OPERATIONAL_IN']+'/'+str(station))
        
        connection.cwd(directory)
        
        for filename in connection.nlst('*10.DAT'):
            fhandle = open(filename, 'wb')
            print ('\t\tDownloading... ' + filename)
            connection.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        print('All files has been downloaded!')
    elif choice == "Anemometric25" or choice =="4":
        pathlib.Path(config_file[0]['OPERATIONAL_IN']+'/'+str(station)).mkdir(parents=True, exist_ok=True)
        os.chdir(config_file[0]['OPERATIONAL_IN']+'/'+str(station))
        
        connection.cwd(directory)
        
        for filename in connection.nlst('*25.DAT'):
            fhandle = open(filename, 'wb')
            print ('\t\tDownloading... ' + filename)
            connection.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        print('All files has been downloaded!')
        
    elif choice == "Anemometric50" or choice =="5":
        pathlib.Path(config_file[0]['OPERATIONAL_IN']+'/'+str(station)).mkdir(parents=True, exist_ok=True)
        os.chdir(config_file[0]['OPERATIONAL_IN']+'/'+str(station))
        
        connection.cwd(directory)
        
        for filename in connection.nlst('*50.DAT'):
            fhandle = open(filename, 'wb')
            print ('\t\tDownloading... ' + filename)
            connection.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        print('All files has been downloaded!')
    elif choice == "b" or choice =="B":
        download_stations()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select one option")
        print("Please try again")
        download_files()

