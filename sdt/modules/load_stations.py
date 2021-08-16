# -*- coding: utf-8 -*-
from modules.load_config import load_config
from modules.top_header import top_header
from modules.load_files import load_files
from camera.process_camera import process_files
from dependecies import *

config = load_config()
inputf = config[0]['TEMPORARY_IN']
inputf2 = config[0]['SKYCAMERA_IN']

def load_stations():
    print(inputf)
    file_names = [fn for fn in listdir(inputf) if not fn.startswith('.')]
    count = -1
    for f in file_names:
        count = count + 1
        print ("\t\t [%s]"  % count + f)
        
    while True:
        try:
            print()
            ans_file = int(input("\t\t Select Station: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_file > count:
            print ("\t\t Wrong selection.")
            continue
    
        station = inputf + file_names[ans_file]
        files = load_files(station)
        break
    
    return files

def load_stations_02():
    file_names = [fn for fn in listdir(inputf2) if not fn.startswith('.')]
    count = -1
    for f in file_names:
        count = count + 1
        print ("\t\t [%s]"  % count + f)
        
    while True:
        try:
            print()
            ans_file = int(input("\t\t Select Station: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_file > count:
            print ("\t\t Wrong selection.")
            continue
    
        station = inputf2 + file_names[ans_file]
        
        files = process_files(station)
        break
    return files

def load_stations_03(path):
    top_header('Qualify Data - Load Stations')
    file_names = [fn for fn in listdir(path) if not fn.startswith('.')]
    file_names.append('ALL')

    count = -1
    for f in file_names:
        count = count + 1
        print ("\t\t [%s]"  % count + f)
    
    while True:
        try:
            ans_file = int(input("\t\t Select Station: "))

            if ans_file > count:
                print ("\t\t Wrong selection.")
                continue

        except:
            print("\t\t Wrong selection")
            continue
        if 'ALL' in file_names[ans_file]:
            types = ['Meteorologicos','Solarimétricos']
            f_file = int(input("\t\t Select type of Data: \n\t\t[0] Meteorologicos\n\t\t[1] Solarimetricos"))
            if f_file == 0:
                fnames = [path+fn+'/Meteorologicos/' for fn in listdir(path) if not fn.startswith('.')]
            if f_file == 1:
                fnames = [path+fn+'/Solarimetricos/' for fn in listdir(path) if not fn.startswith('.')]
            all_paths = []
            for fff in fnames:
                for ff2 in listdir(fff):
                    if not ff2.startswith('.'):
                        all_paths.append(fff+ff2)
            return all_paths

        else:
            station = path + file_names[ans_file]
            return load_stations_04(station)
    
def load_stations_04(path):
    top_header('Select type of Data')
    file_names = [fn for fn in listdir(path) if not fn.startswith('.')]
    count = -1
    for f in file_names:
        count = count + 1
        print ("\t\t [%s]"  % count + f)
        
    while True:
        try:
            print()
            ans_file = int(input("\t\t Select Type of Data: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_file > count:
            print ("\t\t Wrong selection.")
            continue
    
        station = path + '/' + file_names[ans_file]
        return load_stations_05(station)
    
def load_stations_05(path):
    top_header('Select Year')
    file_names = [fn for fn in listdir(path) if not fn.startswith('.')]
    count = -1
    for f in file_names:
        count = count + 1
        print ("\t\t [%s]"  % count + f)
        
    while True:
        try:
            print()
            ans_file = int(input("\t\t Select Station: "))
        except:
            print("\t\t Wrong selection")
            continue
        if ans_file > count:
            print ("\t\t Wrong selection.")
            continue
    
        station = path + '/' + file_names[ans_file]
        return station