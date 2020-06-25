# -*- coding: utf-8 -*-
import sys
from config import DATA_PATH
from os import listdir
from stations import call_station
from menu_header import top_header

def main_menu():
   menu()
   
   
def menu():
    top_header("Main Menu:") 
    choice = input("""
                      1: Anemometric Data
                      2: Solarimetric Data
                      Q: Quit

                      Please enter your choice: """)

    if choice == "Anemometric Data" or choice =="1":
        anemomectric()
    elif choice == "Solarimetric Data" or choice =="2":
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
   pass
    


### Config options
def set_raw_data():
    top_header("Main Menu > Anemometric > Set Raw Data PATH") 
    print()
    global DATA_PATH
    DATA_PATH = input("\t\t Please enter a data path directory:\n")
    print(f'\t\t You entered {DATA_PATH}')
    anemomectric()

def list_config():
    top_header("Main Menu > Anemometric > Data PATH location")
    print()
    print('\t\t Data path is: ',DATA_PATH)
    input("\t\t Press Enter to Back...")
    anemomectric()

def process_data():    
    top_header("Main Menu > Anemometric > Process")
    print()
    
    folder = DATA_PATH
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