# -*- coding: utf-8 -*-
from config import H_TYPES
import glob
import re
import pandas as pd
import numpy as np


def extract_header(station_path,station):

    fsl_ = get_fsl_path(station_path)
    headers = extract_variables(fsl_,station)
    
#    for h in headers:
#        print(','.join(map(str, h[0:10])))

#    
    

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
            
#            print(header[1],header[2])
            station_n =  (','.join(map(str, header[1]))) + '     ' + str(','.join(map(str, header[2])))
            print(station_n)

            ## Variables
            for hd in range(len(header[0])):
                vlues = header[0][hd]['values'].values
                if len(vlues) > 4:
                    varis.append(vlues)
                    
#            print(varis)
            for h in varis:
                print(','.join(map(str, h[0:10])))
            
            
    return varis,header[1]

        
def variables(data):

    full_regex = r"(\w+.csi|\w+.CSI)|(\w+ .+ \w{1}\b)|(\w+:\s+\d+\W\d+\W\d*)"

    
    full_matches = re.finditer(full_regex, data, re.MULTILINE)
    
    ## variables
    vec1 = []
    vec2 = []
    
    fsl_dict = dict(datetime=None,name=None)
    
    vec_ = []
    vec2_ = []
    
    for match in full_matches:
        ### ADD DATETIME GROUP
        if match.group(3) != None:
            vec_.append(match.group(3))
        ### ADD DATETIME GROUP   
        if match.group(1) != None:
            vec2_.append(match.group(1))
        if match.group(2) != None:
            g1 = match.group(2)
            g1 = g1.split(' ')
            cnt,var = g1[0],g1[1]
            vec1.append(int(cnt))
            vec2.append(var)
#            
    
    fsl_dict['datetime'] = vec_
    fsl_dict['name'] = vec2_

    
    ## variables    
    head = pd.DataFrame(index=vec1)
    head['values'] = vec2
    ## datetime


    #groupby sequencial header
    list_of_headers = [d for _, d in head.groupby(head.index - np.arange(len(head)))]

    return list_of_headers,fsl_dict['name'],fsl_dict['datetime']