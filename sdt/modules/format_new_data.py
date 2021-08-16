# -*- coding: utf-8 -*-
from ftplib import FTP
import os # allows me to use os.chdir
from modules.top_header import top_header
import sys
import time
import pathlib

port=21
ip=None
password=None
user=None


def format_data():
    print('format offline')

def format_new_data():
    top_header('Main Menu > Format New Data')
    print('\t\tPlease select an option')
    
    choice = input("""
                  0: Download from FTP
                  1: Offline format
                  Q: Quit
                  Please enter your choice: """)

    if choice == "Download from FTP" or choice =="0":
        connection()
    elif choice == "Offline format" or choice =="1":
        format_data()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either 1 or 2")
        print("Please try again")
    
def connection():
    
    global user,password,ip
    
    top_header(('Main Menu > Format Data > Download Data from FTP'))
    print('\t\tFTP Config:')
    print('\t\tIP: ',ip)
    print('\t\tUser:',user)
    print('\t\tPassword:',password)
    print('\t\tPlease select an option: ')
    
    choice = input("""
                  0: Connect and Download
                  1: Set IP
                  2: Set User
                  3: Set Password
                  B: Back
                  Q: Quit
                  Please enter your choice: """)


    if choice == "Connect" or choice =="0":
       
        print('Connecting....')
        try:
            ftp = FTP(ip)
            ftp.login(user,password)
            time.sleep(2)
            print('Connection established!')
            list_stations(ftp)
        except:
            time.sleep(2)
            print('Connection failed')
            print('Please try again!')
            input()
            connection()


    elif choice == "Set IP" or choice =="1":
        ip = input("\t\tIP:  ")
        connection()
        
    elif choice == "Set User" or choice =="2":
        user = input("\t\tIP:  ")
        connection()
        
    elif choice == "Set Password:" or choice =="3":
        password = input("\t\tPassword:  ")
        connection()
    
    elif choice=="B" or choice=="b":
        format_new_data()
    
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select one option")
        print("Please try again")
        connection()
        
        
def list_stations(ftp):
    
    top_header(('Main Menu > Format Data > Download from FTP > Select station'))
    print('\t\tPlease select an option: \n')
    
    ## FTP Dir
    directory ="/labgama/redesonda/"
    
    ## Add STATIONS
    lt_stations = ['sms','chp','orn']
    
    # direc_st = []
    # for station in ftp.nlst(directory):
    #     if "." in station:
    #         pass
    #     else:
    #         lt_stations.append(station[-3:])
    #         direc_st.append(station)
         
    lt_stations = [x.upper() for x in lt_stations]
    
    count = -1
    for f in lt_stations:
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
        
        lt_stations = [x.lower() for x in lt_stations]
        down_dir = directory + lt_stations[ans_file] + '/data/'
        selected_st = lt_stations[ans_file]
        
        download_data(down_dir,ftp,selected_st)
        break
    
def process_data(temp_dir):
    print(temp_dir)
    
    
def download_data(dow_dir,ftp,st_dir):
    # ## Create dir for temp
    pathlib.Path('../temp/'+st_dir).mkdir(parents=True, exist_ok=True)
    ## Change directory to dowload files
    os.chdir("../temp/"+st_dir)
    ## Change ftp dir
    ftp.cwd(dow_dir)
    for filename in ftp.nlst('*.DAT'):
        fhandle = open(filename, 'wb')
        print ('\t\tDownloading... ' + filename)
        ftp.retrbinary('RETR ' + filename, fhandle.write)
        fhandle.close()
    print('All files has been downloaded!')
    time.sleep(2)
    directory ="/labgama/redesonda/"
    ## Change ftp dir
    ftp.cwd(directory)
    ## Back to connection
    connection()
        
        