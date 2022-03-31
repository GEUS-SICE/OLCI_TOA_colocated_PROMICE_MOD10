#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:51:22 2022

@author: jason

removes columns for old SICE FORTRAN, consolidating the remainder of OLCI_TOA_colocated_PROMICE_MOD10

"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# import statsmodels.api as sm
from numpy.polynomial.polynomial import polyfit
from scipy import stats
from scipy.interpolate import interp1d

meta=pd.read_csv('/Users/jason/Dropbox/AWS/PROMICE/ancil/PROMICE_info_w_header_2017-2018_stats.csv',delim_whitespace=True)
print(meta.columns)
#%%
meta2=pd.read_csv('/Users/jason/Dropbox/S3/ancil/columns_93.txt',delim_whitespace=True,header=None)
print(meta2.iloc[:,1])
#%%
# for site in np.array(meta.name[0:1]).astype(str):
for site in np.array(meta.name).astype(str):
    if site!='NUK_N' and site!='THU_U2' :
        print(site)
        df=pd.read_csv('/Users/jason/Dropbox/S3/output/SICE_FORTRAN/'+site+'_20191108_output.txt',delim_whitespace=True,header=None,names=meta2.iloc[:,1])
        for i,nam in enumerate(meta2.iloc[:,1]):
            # print(i,nam)
            if i>=7 and i<=10:
                # print('dropped')
                df.drop(nam, axis=1, inplace=True)
            if i>=16 and i<=21:
                # print('dropped')
                df.drop(nam, axis=1, inplace=True)
            if i>=43 and i<=84:
                # print('dropped')
                df.drop(nam, axis=1, inplace=True)
        # print(df.columns)
        df.MODIS_albedo[df.MODIS_albedo<0.2]=-999
        df[df==999]=-999
        df.to_csv('/Users/jason/Dropbox/S3/output/SICE_FORTRAN/'+site+'_20191108_output.csv')
#%%
site='SCO_U'
df=pd.read_csv('/Users/jason/Dropbox/S3/output/SICE_FORTRAN/'+site+'_20191108_output.csv')
df["time"]=pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df.index = pd.to_datetime(df.time)
# df[df==999]=np.nan
df[df==-999]=np.nan

fig, ax = plt.subplots(figsize=(14, 14))

plt.plot(df.MODIS_albedo,'.',label='MODIS MOD10A1 BBA')
plt.plot(df.albedo_PROMICE,'.',label='PROMICE BBA')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=90,ha='center' )

plt.legend()