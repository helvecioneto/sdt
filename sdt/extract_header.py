# -*- coding: utf-8 -*-
from config import H_TYPES
import glob
import re
import pandas as pd
import numpy as np


def extract_header(station_path,station):

    fsl_ = get_fsl_path(station_path)
    headers = extract_variables(fsl_,station)
    
    for h in headers:
        print(h)

def get_fsl_path(stat_path):
    files_grabbed = []
    try:
        for file in H_TYPES:
            files_grabbed.extend(glob.glob(stat_path+'/'+file))
    except:
        pass

    ## Add one directory to find fsl
    if len(files_grabbed) == 0:
        try:
            for file in H_TYPES:
                files_grabbed.extend(glob.glob(stat_path+'/*/'+file))
        except:
            pass

    return files_grabbed


def extract_variables(f_list,station):
    
    varis = []
    for it in range(len(f_list)):
        with open(f_list[it]) as file:
            data = file.read()
            header = variables(data)
            
            for hd in range(len(header)):

                vlues = header[hd]['values'].values
                if len(vlues) > 4:
                    varis.append(vlues)

    return varis

        
def variables(data):
    
    regex = r"\w+ .+ \w{1}\b"
    matches = re.finditer(regex, data, re.MULTILINE)
    
    vec1 = []
    vec2 = []

    for match in matches: 
        g1 = match.group()
        g1 = g1.split(' ')
        cnt,var = g1[0],g1[1]
        vec1.append(int(cnt))
        vec2.append(var)
        
    head = pd.DataFrame(index=vec1)   
    head['values'] = vec2

    #groupby sequencial header
    list_of_headers = [d for _, d in head.groupby(head.index - np.arange(len(head)))]

    return list_of_headers