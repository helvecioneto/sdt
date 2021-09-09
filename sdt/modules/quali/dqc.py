from modules.top_header import top_header
from modules.load_config import load_config
from modules.load_files import load_files
from modules.load_stations import load_stations_03
from dependecies import *
from modules.quali.config import *
from pathlib import Path

### DQC LEVELS METEOROLOGICAL
from modules.quali.dqc_met_01 import met_dqc_01
from modules.quali.dqc_met_02 import met_dqc_02
from modules.quali.dqc_met_03 import met_dqc_03


### DQC LEVELS SOLAR
from modules.quali.dqc_sol_01 import sol_dqc_01
#from modules.quali.dqc_sol_02 import sol_dqc_02
#from modules.quali.dqc_sol_03 import sol_dqc_03

## SEM MENUS
def main_qualify():
	out_path = load_config()[0]['QUALI_OUT']
	web_path = load_config()[0]['WEB_OUT']
	files = []
	path_to_qualify = None
	f3 = {p.resolve() for p in Path(load_config()[0]['QUALI_IN']).rglob("**/*" ) if p.suffix in ['.csv']}
	for f4 in f3:
		# Only meteorological
		if '_MD_' in str(f4):
			files.append(Path(f4))
		elif '_SD_' in str(f4):
			files.append(Path(f4))
	# process_files(files,path_to_qualify,out_path,web_path)

def process_files(files,path_to_qualify,out_path,web_path):
	debug_dir = load_config()[0]['DEBUG_DIR']
	debug_di = str(debug_dir) + 'qualify_erros.txt'
	logging.basicConfig(filename=debug_di, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
	# logger.setLevel(logging.INFO)
	# file = '/home/hneto/SONDA/SDT/output/dados_formatados/SBR/Meteorologicos/2016/SBR_2016_06_MD_formatado.csv'
	# file = '/home/hneto/SONDA/SDT/output/dados_formatados/SLZ/Meteorologicos/2017/SLZ_2017_01_MD_formatado.csv'
	count_files = 0
	size_files = len(files)
	for file in files:
#		try:
		### READ DIRECTIONARY
		print('Processing-> ',file.stem[:-6]+ '  -> '+str(count_files)+'/'+str(size_files))
		print('Reading dictionary....!')

		## DETECT TYPE OF DATA
		if '_MD_' in str(file):
			diction,header1,header2 = read_dict('_MD_')
		if '_SD_' in str(file):
			diction,header1,header2 = read_dict('_SD_')

		print('Loading file ->',file.stem)
		df = loadFile(file)
		print('Processing level 01!!')
		dqc,df = level_01(df,str(file),diction)
		print(dqc)
		print(df)


		exit()



		print('Processing level 02!!')
		dqc = level_02(df,dqc,str(file))
		print('Processing level 03!!')
		dqc = level_03(df,dqc,str(file))
		print('Qualify done!...')
		print('Generating percentual file!')

		cols = []
		### SELECT COLUMNS
		for c in dqc.columns:
			if not 'std' in c[0]:
				cols.append(c)
		dqc = dqc[cols]
		percent_columns = dqc.iloc[:,5:].columns

		percent_cols = [cc[0] for cc in percent_columns]
		percent_cols.insert(0, "Dados")
		percentual_df = pd.DataFrame(columns=percent_cols)
		percentual_df['Dados'] = ['Suspeitos nível 1','Suspeitos nível 2','Suspeitos nível 3','Suspeitos nível 4','Válidos','Ausentes']
		percentual_df = percentual_df.fillna(0)

		#Perc Válido (2)
		VALID_STRING = "9999|0999|0099|0009"
		## AUSENTES
		NODATA = "3333"
		NOSENSOR = "-5555"
		## SUPECT LEVELS
		SUSPECT_LVL1 = "5552|0552|0052|0002"
		SUSPECT_LVL2 = "5529|0529|0029"
		SUSPECT_LVL3 = "5299|0299"
		SUSPECT_LVL4 = "2999"

		for pc in percent_columns:
			nosensor = df[pc[0]].astype(str).str.count(NOSENSOR).sum()
			if nosensor > 0:
				percentual_df[pc[0]] = ['N/S','N/S','N/S','N/S','N/S','N/S']
			else:
				valids = dqc[pc].str.count(VALID_STRING).sum()
				susplvl1 = dqc[pc].str.count(SUSPECT_LVL1).sum()
				susplvl2 = dqc[pc].str.count(SUSPECT_LVL2).sum()
				susplvl3 = dqc[pc].str.count(SUSPECT_LVL3).sum()
				susplvl4 = dqc[pc].str.count(SUSPECT_LVL4).sum()
				nodata = df[pc[0]].astype(str).str.count(NODATA).sum()
				total_ = valids + susplvl1 + susplvl2 + susplvl3 + susplvl4 + nodata
				## ADD IN PERCENTUAL FRAME
				percentual_df[pc[0]] = [susplvl1/total_,
										susplvl2/total_,
										susplvl3/total_,
										susplvl4/total_,
										valids/total_,
										nodata/total_]
		## WEB FILE
		web_df = pd.DataFrame()
		station = df.acronym.unique()[0]
		stationID = diction.loc[diction['Sigla'] == station]
		siglaNAME = stationID['Sigla'].values[0]
		nomeNAME = stationID['Nome'].values[0]
		redeNAME = stationID['Rede'].values[0]
		latNAME = stationID['Latitude'].values[0]
		lonNAME = stationID['Longitude'].values[0]
		altNAME = stationID['Altitude'].values[0]

		first_row_header = [siglaNAME,nomeNAME,'lat:'+str(latNAME),'lon:'+str(lonNAME),'alt:'+str(altNAME)+'m',redeNAME+' Network','http://sonda.ccst.inpe.br','sonda@inpe.br']

		### INCREMENT columns into dqc frame
		dqc['ws10_std','dqc_v1'] = '0000'
		dqc['wd10_std','dqc_v1'] = '0000'

		dqc_cols = []
		dqc_mult_column = []
		dqc_columns = dqc.columns.values
		dqc_columns = [dqc_cols.append(c[0]) for c in dqc_columns]
		for cc in range(len(dqc_cols)):
			if cc > 4:
				dqc_cols[cc] = dqc_cols[cc]+'_dqc'
				dqc_mult_column.append((dqc_cols[cc],'dqc_v1'))
			else:
				dqc_mult_column.append((dqc_cols[cc],''))
		mux = pd.MultiIndex.from_tuples(dqc_mult_column)

		dqc.columns = dqc_cols
		dqc_for_concat = dqc[dqc_cols[5:]]
		dqc.columns = mux

		# ### WEB FILE
		web_df = pd.concat([df,dqc_for_concat],axis=1)
		web_df = web_df[header1.tolist()]

		## MOUNT NEW MULTINDEX
		header2 = header2.tolist()
		header2.insert(0,'')
		header2.insert(0,'')
		header2.insert(0,'')
		header2.insert(0,'')
		header2.insert(0,'')

		new_mux = []
		for cc in range(len(web_df.columns)):
			if cc < len(first_row_header):
				new_mux.append((first_row_header[cc],web_df.columns[cc],header2[cc]))
			else:
				new_mux.append(('',web_df.columns[cc],header2[cc]))

		mux = pd.MultiIndex.from_tuples(new_mux)
		# ## FINALIZE WEB DF
		web_df.columns = mux

		### CONVERT VALUES TO STRING
		all_columns = list(web_df) # Creates list of all column headers
		web_df[all_columns] = web_df[all_columns].astype(str)

		### - Alterar 3333 = N/A antes de salvar o arquivo
		### - Alterar -5555 = N/S antes de salvar o arquivo (linha 170 arquivo dqc.py)

		web_df = web_df.replace('3333.0', 'N/A')
		web_df = web_df.replace('-5555', 'N/S')

		print(web_df)

		print('Saving file...')
		### SAVE FILES
		if type(path_to_qualify) == str:
			mount_out = Path(path_to_qualify).parts[2:]
		else:
			mount_out = Path(file).parts[-4:][:-1]
		mount_out = '/'.join([str(elem) for elem in mount_out])
		### CREATE PAATH IF NOT EXIST
		Path(out_path+mount_out+'/').mkdir(parents=True, exist_ok=True)
		output_file = out_path+mount_out+'/'+file.stem[:-9]+'DQC'+file.suffix
		## SALVANDO
		dqc.to_csv(output_file,index=False)

		### WEB FILES
		web_csv = web_path+mount_out
		Path(web_path+mount_out+'/').mkdir(parents=True, exist_ok=True)
		output_web = web_path+mount_out+'/'+file.stem[:-10]+file.suffix
		percentual_out = web_path+mount_out+'/'+file.stem[:-9]+'percentuais'+file.suffix
		### SAVING
		web_df.to_csv(output_web,index=False)
		percentual_df.to_csv(percentual_out,index=False)
		print('Files has been saved into->',output_file,'\nWEB->',output_web)
		count_files += 1
#		except:
#			print('Error to qualify file: '+str(file))
#			logging.warning('Error to qualify file: '+str(file)+'')
#			count_files += 1


#### GLOBAL VARIABLES
def menu_qualify():
	top_header('Qualify SONDA Data->')
	path_to_qualify = load_stations_03(load_config()[0]['QUALI_IN'])
	out_path = load_config()[0]['QUALI_OUT']
	web_path = load_config()[0]['WEB_OUT']

	if type(path_to_qualify) == str:
		files = {p.resolve() for p in Path(path_to_qualify).rglob("**/*" ) if p.suffix in ['.csv']}
	else:
		files = []
		for f2 in path_to_qualify:
			f3 = {p.resolve() for p in Path(f2).rglob("**/*" ) if p.suffix in ['.csv']}
			for f4 in f3:
				files.append(Path(f4))

	process_files(files,path_to_qualify,out_path,web_path)

def read_dict(type_of_data):
    # Ler dicitionario
    dicionario = pd.read_excel(open(load_config()[0]['DICTIONARY'], 'rb'),sheet_name='Tabela-estacao')
    colunas_dicionario = pd.read_excel(open(load_config()[0]['DICTIONARY'], 'rb'),sheet_name='Cabeçalhos SONDA',header=None)
    
    if type_of_data == '_MD_':
        header_1 = colunas_dicionario.iloc[29:30]
        header_1 = header_1.iloc[0].dropna().values[1:]
        header_2 = colunas_dicionario.iloc[30:31]        
        header_2 = header_2.iloc[0].dropna().values[1:]

    if type_of_data == '_SD_':
    	header_1 = colunas_dicionario.iloc[12:13].iloc[0].dropna().values[1:]
    	header_2 = colunas_dicionario.iloc[13:14].iloc[0].dropna().values[1:]
    return dicionario,header_1,header_2

def loadFile(path):
    df = pd.read_csv(path, header=[0, 1])
    cols = []
    for c in df.columns:
        if 'Unnamed' in c[1]:
            c_ = ''
        else:
            c_ = c[1]
        cols.append((c[0],c_))
    mux = pd.MultiIndex.from_tuples(cols)
    df.columns = mux
    ## Transforma coluna temporal
    df['timestamp'] = pd.to_datetime(df.timestamp, format='%Y-%m-%d %H:%M:%S')
    return df

### CALL LEVEL 01
def level_01(dframe01,type_,dict):
    if '_MD_' in type_:
        dqc_df01 = met_dqc_01(dframe01,dict)
        return dqc_df01
    if '_SD_' in type_:
    	dqc_df01 = sol_dqc_01(dframe01,dict)
    	return dqc_df01

### CALL LEVEL 02
def level_02(dframe02,dqc_frame02,type_= None):
    if '_MD_' in type_:
        ### Abrir frame passado
        past_path_year = (dframe02.iloc[0]['timestamp'] - np.timedelta64(1, "M")).year
        past_path_month = (dframe02.iloc[0]['timestamp'] - np.timedelta64(1, "M")).strftime('%Y_%m')
        past_path =  str(Path(type_).parent.parent) + '/' + str(past_path_year) + '/' + Path(type_).parts[-1][0:4] + past_path_month + Path(type_).parts[-1][11:]
        dqc_df02 = met_dqc_02(dframe02,dqc_frame02,past_path)
    return dqc_df02

### CALL LEVEL 03
def level_03(dframe03,dqc_frame03,type_= None):
    if '_MD_' in type_:
        ### Abrir frame passado
        past_path_year = (dframe03.iloc[0]['timestamp'] - np.timedelta64(1, "M")).year
        past_path_month = (dframe03.iloc[0]['timestamp'] - np.timedelta64(1, "M")).strftime('%Y_%m')
        past_path =  str(Path(type_).parent.parent) + '/' + str(past_path_year) + '/' + Path(type_).parts[-1][0:4] + past_path_month + Path(type_).parts[-1][11:]
        dqc_df03 = met_dqc_03(dframe03,dqc_frame03,past_path)
    return dqc_df03


