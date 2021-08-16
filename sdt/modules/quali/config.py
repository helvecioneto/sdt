from dependecies import *

### LOAD CONFIGS
## CARREGAR LIMITES
temp_min = pd.read_table('./sdt2/modules/quali/limites/temp.min',sep=',',header=None,names=['id','01','02','03','04','05','06','07','08','09','10','11','12'])
temp_max = pd.read_table('./sdt2/modules/quali/limites/temp.max',sep=',',header=None,names=['id','01','02','03','04','05','06','07','08','09','10','11','12'])
press_max = pd.read_table('./sdt2/modules/quali/limites/press.max',sep=',',header=None,names=['id','max'])
press_min = pd.read_table('./sdt2/modules/quali/limites/press.min',sep=',',header=None,names=['id','min'])
rain_max = pd.read_table('./sdt2/modules/quali/limites/rain.max',sep=',',header=None,names=['id','01','02','03','04','05','06','07','08','09','10','11','12'])