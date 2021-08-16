# -*- coding: utf-8 -*-
#from modules.load_config import load_config
from os import listdir
from modules.top_header import top_header
from camera.process_camera import process_files
from pathlib import Path

def load_files(path):
    top_header(path)
    years_ = [fn for fn in listdir(path) if fn.startswith('2')]
    years_.sort()

    count = -1
    for f in years_:
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
        
        path = path + '/' +years_[ans_file] + '/'
        files = get_files(path)
        break
    return files
    
def get_files(path):
    files = {p.resolve() for p in Path(path).rglob("**/*" ) if p.suffix in ['.dat']}
    return files

def get_files_02(path):
    files = {p.resolve() for p in Path(path).rglob("**/*" ) if p.suffix in ['.txt']}
    return files


def load_files_02(path):
    lista_files = get_files_02(path)
    process_files(lista_files)