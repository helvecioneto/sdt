# -*- coding: utf-8 -*-
import sys
import os
from config import DATA_PATH

def main_menu():
   menu()
   
def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("************Welcome to Sonda Data Translator V1.0**************")
    print("***************************************************************")
    print("************Please Select data type to translate***************")
    print()
    
    choice = input("""
                      1: Anemometric Data
                      2: Solarimetric Data
                      Q: Logout

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
    os.system('cls' if os.name == 'nt' else 'clear')
    print("************Welcome to Sonda Data Translator V1.0**************")
    print("***************************************************************")
    print("********************Anemometric Data***************************")
    print()
    choice = input("""
                      1: Set location of Raw Data
                      2: List Path in config file
                      B: Back...

                      Please enter your choice: """)

    if choice == "Set location of Raw Data" or choice =="1":
        set_raw_data()
    elif choice == "List Path in config file" or choice =="2":
        list_config()
    elif choice=="B" or choice=="b":
        menu()()
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        print("You must only select either 1 or 2")
        print("Please try again")
        anemomectric()
    
def solarimetric():
   pass
    


### Config options
def set_raw_data():
    print('Selecionar ')
    pass

def list_config():
    print(DATA_PATH)
    pass