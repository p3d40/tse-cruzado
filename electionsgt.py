#Import other libraries
import pandas as pd
import geopandas as gpd
from os import listdir
from os.path import isfile, join
import numpy as np
import scipy.stats
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.colors as colors
from matplotlib.colors import LinearSegmentedColormap
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
import math
from unidecode import unidecode
from PIL import Image
import seaborn as sns
#Data files
DATA_PLOT='shape_gtm/'
FILE_DEPTS='departamentos_gtm.shp'
FILE_MUNS='municipios_gtm.shp'
DATA_DIR='GTM-pruebas/'
PRE_DIR='1-PRESIDENTE/'
DNC_DIR='2-DIP-NAC/'
DDT_DIR='3-DIP-DIST/'
MUN_DIR='4-CORPORACIÓN/'
PAR_DIR='5-DIP-PAR/'
#Image properties
plt.rcParams['figure.figsize'] = [16, 9]
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Lucida Grande']
#Geopandas
dfg_depts = gpd.read_file(DATA_PLOT+FILE_DEPTS)
dfg_muns = gpd.read_file(DATA_PLOT+FILE_MUNS)
#Cleaning dataframes
pre_files = [f for f in listdir(DATA_DIR+PRE_DIR) if isfile(join(DATA_DIR+PRE_DIR, f))]
dnc_files = [f for f in listdir(DATA_DIR+DNC_DIR) if isfile(join(DATA_DIR+DNC_DIR, f))]
ddt_files = [f for f in listdir(DATA_DIR+DDT_DIR) if isfile(join(DATA_DIR+DDT_DIR, f))]
mun_files = [f for f in listdir(DATA_DIR+MUN_DIR) if isfile(join(DATA_DIR+MUN_DIR, f))]
par_files = [f for f in listdir(DATA_DIR+PAR_DIR) if isfile(join(DATA_DIR+PAR_DIR, f))]
try:
    del df_pre
except:
    pass
try:
    del df_dnc
except:
    pass
try:
    del df_ddt
except:
    pass
try:
    del df_mun
except:
    pass
try:
    del df_par
except:
    pass
df_pre = pd.DataFrame()
df_dnc = pd.DataFrame()
df_ddt = pd.DataFrame()
df_mun = pd.DataFrame()
df_par = pd.DataFrame()

for file in pre_files:
    df_pre=pd.concat([df_pre,pd.read_csv(DATA_DIR+PRE_DIR+file,skiprows=5)], ignore_index=True)
for file in dnc_files:
    df_dnc=pd.concat([df_dnc,pd.read_csv(DATA_DIR+DNC_DIR+file,skiprows=5)], ignore_index=True)
for file in ddt_files:
    df_ddt=pd.concat([df_ddt,pd.read_csv(DATA_DIR+DDT_DIR+file,skiprows=5)], ignore_index=True)
for file in mun_files:
    df_mun=pd.concat([df_mun,pd.read_csv(DATA_DIR+MUN_DIR+file,skiprows=5)], ignore_index=True)
for file in par_files:
    df_par=pd.concat([df_par,pd.read_csv(DATA_DIR+PAR_DIR+file,skiprows=5)], ignore_index=True)

df_pre = df_pre.fillna(0)
df_dnc = df_dnc.fillna(0)
df_ddt = df_ddt.fillna(0)
df_mun = df_mun.fillna(0)
df_par = df_par.fillna(0)
partidos_pre=list(df_pre.columns[7:29])
for partido in partidos_pre:
    df_pre[partido] = df_pre[partido].replace({'--':0})
    df_pre[partido] = df_pre[partido].astype(int)

df_pre['NULOS'] = df_pre['NULOS'].replace({'--':0})
df_pre['NULOS'] = df_pre['NULOS'].astype(int)
df_dnc['NULOS'] = df_dnc['NULOS'].replace({'--':0})
df_dnc['NULOS'] = df_dnc['NULOS'].astype(int)
df_ddt['NULOS'] = df_ddt['NULOS'].replace({'--':0})
df_ddt['NULOS'] = df_ddt['NULOS'].astype(int)
df_mun['NULOS'] = df_mun['NULOS'].replace({'--':0})
df_mun['NULOS'] = df_mun['NULOS'].astype(int)
df_par['NULOS'] = df_par['NULOS'].replace({'--':0})
df_par['NULOS'] = df_par['NULOS'].astype(int)

df_pre['VÁLIDOS'] = df_pre['VÁLIDOS'].replace({'--':0})
df_pre['VÁLIDOS'] = df_pre['VÁLIDOS'].astype(int)
df_dnc['VÁLIDOS'] = df_dnc['VÁLIDOS'].replace({'--':0})
df_dnc['VÁLIDOS'] = df_dnc['VÁLIDOS'].astype(int)
df_ddt['VÁLIDOS'] = df_ddt['VÁLIDOS'].replace({'--':0})
df_ddt['VÁLIDOS'] = df_ddt['VÁLIDOS'].astype(int)
df_mun['VÁLIDOS'] = df_mun['VÁLIDOS'].replace({'--':0})
df_mun['VÁLIDOS'] = df_mun['VÁLIDOS'].astype(int)
df_par['VÁLIDOS'] = df_par['VÁLIDOS'].replace({'--':0})
df_par['VÁLIDOS'] = df_par['VÁLIDOS'].astype(int)

df_pre['TOTAL'] = df_pre['TOTAL'].replace({'--':0})
df_pre['TOTAL'] = df_pre['TOTAL'].astype(int)
df_dnc['TOTAL'] = df_dnc['TOTAL'].replace({'--':0})
df_dnc['TOTAL'] = df_dnc['TOTAL'].astype(int)
df_ddt['TOTAL'] = df_ddt['TOTAL'].replace({'--':0})
df_ddt['TOTAL'] = df_ddt['TOTAL'].astype(int)
df_mun['TOTAL'] = df_mun['TOTAL'].replace({'--':0})
df_mun['TOTAL'] = df_mun['TOTAL'].astype(int)
df_par['TOTAL'] = df_par['TOTAL'].replace({'--':0})
df_par['TOTAL'] = df_par['TOTAL'].astype(int)

df_pre['EMITIDOS'] = df_pre['EMITIDOS'].replace({'--':0})
df_pre['EMITIDOS'] = df_pre['EMITIDOS'].astype(int)
df_dnc['EMITIDOS'] = df_dnc['EMITIDOS'].replace({'--':0})
df_dnc['EMITIDOS'] = df_dnc['EMITIDOS'].astype(int)
df_ddt['EMITIDOS'] = df_ddt['EMITIDOS'].replace({'--':0})
df_ddt['EMITIDOS'] = df_ddt['EMITIDOS'].astype(int)
df_mun['EMITIDOS'] = df_mun['EMITIDOS'].replace({'--':0})
df_mun['EMITIDOS'] = df_mun['EMITIDOS'].astype(int)
df_par['EMITIDOS'] = df_par['EMITIDOS'].replace({'--':0})
df_par['EMITIDOS'] = df_par['EMITIDOS'].astype(int)

df_pre['PADRÓN'] = df_pre['PADRÓN'].replace({'--':0})
df_pre['PADRÓN'] = df_pre['PADRÓN'].astype(int)

df_pre['PAPELETAS-RECIBIDAS'] = df_pre['PAPELETAS-RECIBIDAS'].replace({'--':0})
df_pre['PAPELETAS-RECIBIDAS'] = df_pre['PAPELETAS-RECIBIDAS'].astype(int)
df_pre['PAPELETAS-NO-USADAS'] = df_pre['PAPELETAS-NO-USADAS'].replace({'--':0})
df_pre['PAPELETAS-NO-USADAS'] = df_pre['PAPELETAS-NO-USADAS'].astype(int)
#Geopandas paring
df_pre['CODIGO_MUN']={}
for index, row in df_pre.iterrows():
    if (row['DEPARTAMENTO']=='Distrito Central'):
        df_pre.at[index,'CODIGO_MUN']=int(row['ID_DEPARTAMENTO']+1)*100+int(row['ID_MUNICIPIO'])
    else:
        df_pre.at[index,'CODIGO_MUN']=int(row['ID_DEPARTAMENTO'])*100+int(row['ID_MUNICIPIO'])
df_dnc['CODIGO_MUN']={}
for index, row in df_dnc.iterrows():
    if (row['DEPARTAMENTO']=='Distrito Central'):
        df_dnc.at[index,'CODIGO_MUN']=int(row['ID_DEPARTAMENTO']+1)*100+int(row['ID_MUNICIPIO'])
    else:
        df_dnc.at[index,'CODIGO_MUN']=int(row['ID_DEPARTAMENTO'])*100+int(row['ID_MUNICIPIO'])
df_ddt['CODIGO_MUN']={}
for index, row in df_ddt.iterrows():
    if (row['DEPARTAMENTO']=='Distrito Central'):
        df_ddt._set_value(index,'CODIGO_MUN',int(row['ID_DEPARTAMENTO']+1)*100+int(row['ID_MUNICIPIO']))
    else:
        df_ddt._set_value(index,'CODIGO_MUN',int(row['ID_DEPARTAMENTO'])*100+int(row['ID_MUNICIPIO']))
#Definitions
df_total=df_pre[['EMITIDOS','CODIGO_MUN']].groupby(df_pre['CODIGO_MUN']).sum().copy()
df_sca=df_pre[partidos_pre+['CODIGO_MUN']].groupby(df_pre['CODIGO_MUN']).sum().copy()
df_nor=df_sca[partidos_pre].div(df_total['EMITIDOS'], axis=0).copy().fillna(0)

order=list(df_nor.mean(axis=0).sort_values(ascending=False).index)
partidos_dnc=list(df_dnc.columns[7:33])
for partido in partidos_dnc:
    df_dnc[partido] = df_dnc[partido].replace({'--':0})
    #print(partido)
    df_dnc[partido] = df_dnc[partido].astype(int)
partidos_ddt=list(df_ddt.columns[7:33])+list(df_ddt.columns[50:])#+['NULOS']
for partido in partidos_ddt:
    df_ddt[partido] = df_ddt[partido].replace({'--':0})
    df_ddt[partido] = df_ddt[partido].astype(int)
#Geopandas definitions
def plot_depts(series):
    try:
        del dfg_temp
    except:
        pass
    dfg_temp=dfg_depts.copy()
    dfg_temp['graph']={}
    for index, value in series.items():
        try:
            idx=dfg_temp[dfg_temp['nombre']==unidecode(index.upper())].index[0]
            dfg_temp['graph'].iloc[idx]=value
        except:
            pass
    return dfg_temp
def plot_depts_sum(series):
    try:
        del dfg_temp
    except:
        pass
    dfg_temp=dfg_depts.copy()
    dfg_temp['graph']={}
    for index, value in series.items():
        try:
            idx=dfg_temp[dfg_temp['nombre']==unidecode(index.upper())].index[0]
            dfg_temp['graph'].iloc[idx]=value
        except:
            pass
    idg=dfg_depts[dfg_depts['nombre']=='GUATEMALA'].index[0]
    dfg_temp['graph'].iloc[idg]+=series['Distrito Central']
    return dfg_temp
def plot_depts_rat(series):
    try:
        del dfg_temp
    except:
        pass
    dfg_temp=dfg_depts.copy()
    dfg_temp['graph']={}
    for index, value in series.items():
        try:
            idx=dfg_temp[dfg_temp['nombre']==unidecode(index.upper())].index[0]
            dfg_temp['graph'].iloc[idx]=value
        except:
            pass
    idg=dfg_depts[dfg_depts['nombre']=='GUATEMALA'].index[0]
    dfg_temp['graph'].iloc[idg]=(dfg_temp['graph'].iloc[idg]+series['Distrito Central'])/2
    return dfg_temp
