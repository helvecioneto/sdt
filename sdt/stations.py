# -*- coding: utf-8 -*-
from os import listdir
from extract_header import extract_header
from menu_header import top_header

def call_station(path,station):
    print()
    top_header("Main Menu > Anemometric > Process > " + str(station))
    print()
    
    path = path+station
    # Path to fsl extract
    path_ = path
    years_ = [fn for fn in listdir(path) if fn.startswith('2')]
    
    count = -1
    for f in years_:
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
        
        path = path + '/' +years_[ans_file] + '/'
        

        extract_header(path_,station)

        break
    
