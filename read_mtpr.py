# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 17:38:09 2021

@author: Renata
"""

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

#%% 
ds = xr.open_mfdataset('precip_era5_mean_*.nc', parallel=True) #abre múltiplos arquivos

month = ds.groupby("time")
mtpr = ds['mtpr']
time = ds['time']

#%% ploting contourf

fg = mtpr.plot.contourf(
    col="time",
    col_wrap=4,
    levels=28
    )

#%% Choosing a point at North and South


north = mtpr.sel(longitude=297,latitude=18.75).plot()
south = mtpr.sel(longitude=297,latitude=17.5).bar.plot()




