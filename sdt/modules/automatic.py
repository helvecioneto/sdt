# -*- coding: utf-8 -*-
from modules.top_header import top_header
from modules.load_config import load_config
from pathlib import Path
import numpy as np
import pandas as pd
import sys

config = load_config()
path_ = config[0]['AUTO_DATA']

def load_data_type():
    top_header('Main Menu > Automatic Detection')
    print('\t\tPlease select an option: ')
    print('\t\tPath dir: ',path_)
    choice = input("""
                  1: Detect Solarimetric Data
                  2: Detect Meteorological Data
                  3: Detect Anemometric Data
                  4: Detect Sky Camera Data
                  5: Set Data PATH
                  Q: Quit
                  Please enter your choice: """)

    if choice == "Detect Solarimetric Data" or choice =="1":
        detec_solar()
    elif choice == "Detect Meteorological Data" or choice =="2":
        detect_met()
    elif choice == "Detect Anemometric Data" or choice =="3":
        detect_ane()
    elif choice == "Detect Sky Camera Data" or choice =="4":
        detect_sky()
    elif choice == "Set Data PATH" or choice =="5":
        set_path()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select one option")
        print("Please try again")
        load_data_type()
        
def detec_solar():
    files = {p.resolve() for p in Path(path_).rglob("**/*" ) if p.suffix in ['.DAT']}

    ftype = "SD"
    ## SEPARET FILES BY TYPE
    s_files = []    
    for f in files:
        if (ftype in f.name):
            s_files.append(f)
    
    ## SEPARATE FILES BY STATION
    st_fi = []
    for s in sorted(s_files):
        st_fi.append(s.name[:3])
    st_uni = np.unique(np.array(st_fi))
    
    stat_, sfiles_ = find_files(st_uni,s_files)
    year_ = find_fyears(stat_,sfiles_)
    
    ## Process files
    for f in year_[0]:
        process_files(stat_,year_[1],f,ftype) 
    
def detect_met():
    files = {p.resolve() for p in Path(path_).rglob("**/*" ) if p.suffix in ['.DAT']}

    ftype = "MD"
    ## SEPARET FILES BY TYPE
    s_files = []    
    for f in files:
        if (ftype in f.name):
            s_files.append(f)
    
    ## SEPARATE FILES BY STATION
    st_fi = []
    for s in sorted(s_files):
        st_fi.append(s.name[:3])
    st_uni = np.unique(np.array(st_fi))
    
    stat_, sfiles_ = find_files(st_uni,s_files)
    year_ = find_fyears(stat_,sfiles_)
    
    ## Process files
    for f in year_[0]:
        process_files(stat_,year_[1],f,ftype)

def detect_ane():
    files = {p.resolve() for p in Path(path_).rglob("**/*" ) if p.suffix in ['.DAT']}

    ftype = "WD"
    ## SEPARET FILES BY TYPE
    s_files = []    
    for f in files:
        if (ftype in f.name):
            s_files.append(f)
    
    ## SEPARATE FILES BY STATION
    st_fi = []
    for s in sorted(s_files):
        st_fi.append(s.name[:3])
    st_uni = np.unique(np.array(st_fi))
    
    stat_, sfiles_ = find_files(st_uni,s_files)
    year_ = find_fyears(stat_,sfiles_)
    
    ## Process files
    for f in year_[0]:
        process_files(stat_,year_[1],f,ftype)

def detect_sky():
    pass

def set_path():
    global path_
    path_ = input("\t\tPlease type PATH directory: ")
    load_data_type()
    
def find_files(st_uni,s_files):
    ## Detect stations
    top_header('Main Menu > Automatic Detection > Solar Data')
    print('\t\tPlease select on station option: \n')
    print('\t\tNumber of stations found: \t',len(st_uni))
    print('\t\tNumber of files:   \t\t',len(s_files))
    print('\n')
    
    count = -1
    for f in st_uni:
        count = count + 1
        num_fils = []
        for fis in s_files:
            if (f in fis.name):
                num_fils.append(fis)
        print ("\t\t [%s]"  % count + f + '  files -> '+ str(len(num_fils)))
        
    while True:
        try:
            ans_st = int(input("\n\t\t Select Station: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_st > count:
            print ("\t\t Wrong selection.")
            continue
        
        station_files = []
        for fff in s_files:
            if (st_uni[ans_st] in fff.name):
                station_files.append(fff)
        
        return st_uni[ans_st],station_files
        break
    
def find_fyears(stat_,sfiles_):
    top_header('Main Menu > Automatic Detection > Solar Data > Station: '+str(stat_))
    print('\t\tPlease select on year to process: \n')
    print('\n')
    
    ## Filter years
    yrs = []
    for f in sfiles_:
        yrs.append(f.name[4:8])
    st_yrs = np.unique(np.array(yrs))
    
    count = -1
    for f in st_yrs:
        count = count + 1
        num_fils = []
        for fis in sfiles_:
            if (f in fis.name):
                num_fils.append(fis)
        print ("\t\t [%s]"  % count + f + '  files -> '+ str(len(num_fils)))
    while True:
        try:
            ans_file = int(input("\t\t Select Station: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_file > count:
            print ("\t\t Wrong selection.")
            continue
        
        path = st_yrs[ans_file]
        yearFiles = []
        for ffy in sfiles_:
            if (st_yrs[ans_file] in ffy.name):
                yearFiles.append(ffy)
        return yearFiles, path
        break
    
def process_files(stat_,year_,file,ftype):
    
    if ftype == 'WD':
        print(stat_,year_,file,ftype)
        df1 = pd.read_csv(file, sep=",", header=None, skiprows=4,skipinitialspace=False)
        head = pd.read_csv(file,sep=",",header=None, skiprows=1,nrows = 1)
        head2 = pd.read_csv(file,sep=",",header=None, skiprows=3,nrows = 1)
        head = head.iloc[0].values
        head2 = head2.iloc[0].values
        
        ## Transform timestamp
        df1[0] = pd.to_datetime(df1[0] , format='%Y-%m-%d %H:%M:%S')
        
        ## Create multindex columns
        mux = []
        for i in range(len(head)):
            mux.append([str(head[i]).lower(),str(head2[i]).lower()])
        mux = pd.MultiIndex.from_tuples(mux)
        df1.columns = mux
        print(df1)
        input()
        
    if ftype == 'SD':
        print(stat_,year_,file,ftype)
        df1 = pd.read_csv(file, sep=",", header=None, skiprows=4,skipinitialspace=False)
        head = pd.read_csv(file,sep=",",header=None, skiprows=1,nrows = 1)
        head2 = pd.read_csv(file,sep=",",header=None, skiprows=3,nrows = 1)
        head = head.iloc[0].values
        head2 = head2.iloc[0].values
        
        ## Transform timestamp
        df1[0] = pd.to_datetime(df1[0] , format='%Y-%m-%d %H:%M:%S')
        
        ## Create multindex columns
        mux = []
        for i in range(len(head)):
            mux.append([str(head[i]).lower(),str(head2[i]).lower()])
        mux = pd.MultiIndex.from_tuples(mux)
        df1.columns = mux
        print(df1)
        input()