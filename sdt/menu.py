# -*- coding: utf-8 -*-
import sys
from config import EOLIC_DATA, SOLAR_DATA
from os import listdir
from sts import call_station, call_station_solar
from menu_header import top_header

def main_menu():
   menu()
   
   
def menu():
    top_header("Main Menu:") 
    choice = input("""
                      1: Anemometric Data
                      2: Solar Data
                      Q: Quit

                      Please enter your choice: """)

    if choice == "Anemometric Data" or choice =="1":
        anemomectric()
    elif choice == "Solar Data" or choice =="2":
        solarimetric()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either 1 or 2")
        print("Please try again")
        menu()
        
def anemomectric():
    top_header("Main Menu > Anemometric")
    choice = input("""
                      1: Process Data
                      2: List Path in config file
                      3: Set location of Raw Data
                      B: Back
                      Q: Quit

                      Please enter your choice: """)

    if choice == "Process data" or choice =="1":
        process_data()
    elif choice == "Set location of Raw Data" or choice =="3":
        set_raw_data()
    elif choice == "List Path in config file" or choice =="2":
        list_config()
    elif choice=="B" or choice=="b":
        menu()()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either 1, 2 or 3")
        print("Please try again")
        anemomectric()
    
def solarimetric():
    top_header("Main Menu > Solar")
    choice = input("""
                      1: Process Data
                      2: List Path in config file
                      3: Set location of Raw Data
                      B: Back
                      Q: Quit

                      Please enter your choice: """)

    if choice == "Process data" or choice =="1":
        process_data_solar()
    elif choice == "Set location of Raw Data" or choice =="3":
        set_raw_data_solar()
    elif choice == "List Path in config file" or choice =="2":
        list_config_solar()
    elif choice=="B" or choice=="b":
        menu()()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either 1, 2 or 3")
        print("Please try again")
        solarimetric()
    

### Config options
def set_raw_data():
    top_header("Main Menu > Anemometric > Set Raw Data PATH") 
    print()
    global EOLIC_DATA
    EOLIC_DATA = input("\t\t Please enter a data path directory:\n")
    print(f'\t\t You entered {EOLIC_DATA}')
    anemomectric()

def list_config():
    top_header("Main Menu > Anemometric > Data PATH location")
    print()
    print('\t\t Data path is: ',EOLIC_DATA)
    input("\t\t Press Enter to Back...")
    anemomectric()

def process_data():    
    top_header("Main Menu > Anemometric > Process")
    print()
    
    folder = EOLIC_DATA
    file_names = [fn for fn in listdir(folder) if not fn.startswith('.')]

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

        path = folder + file_names[ans_file]
        print ("\t\t Selected file: %s " % path)
        call_station(folder,file_names[ans_file])
        break
    
### SOLAR
def process_data_solar():
    top_header("Main Menu > Solar > Process")
    print()
    
    folder = SOLAR_DATA
    file_names = [fn for fn in listdir(folder) if not fn.startswith('.')]

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

        path = folder + file_names[ans_file]
        print ("\t\t Selected file: %s " % path)
        call_station_solar(folder,file_names[ans_file])
        break
    
def set_raw_data_solar():
    top_header("Main Menu > Solar > Set Raw Data PATH") 
    print()
    global SOLAR_DATA
    SOLAR_DATA = input("\t\t Please enter a data path directory:\n")
    print(f'\t\t You entered {SOLAR_DATA}')
    anemomectric()

def list_config_solar():
    top_header("Main Menu > Solar > Data PATH location")
    print()
    print('\t\t Data path is: ',SOLAR_DATA)
    input("\t\t Press Enter to Back...")
    solarimetric()