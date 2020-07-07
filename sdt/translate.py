# -*- coding: utf-8 -*-
#from config import SOLAR_DATA
from stations.brb import translate_brb

def translate_station(df,path):
    
    if 'BRB' in str(path):
        translate_brb(df)
