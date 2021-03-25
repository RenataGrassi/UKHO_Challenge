# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 20:04:38 2021

@author: Renata
"""
import xarray as xr

ds = xr.open_mfdataset('sea_and_swell_era5_mean_*.nc', parallel=True) # abre todos os arquivos de onda na pasta
ds # visualiza informações
swh = ds['swh'] # separa os dados de interesse
merged = xr.merge([ds],compat="no_conflicts") # faz merge dos datasets 

merged.to_netcdf('C:/Users/55219/Documents/teste_netcdf.nc') #escolhe caminho e nome do arquivo a ser gerado e salvo

ds2 = xr.open_dataset('teste_netcdf.nc') #abre só o arquivo que geramos
xr.DataArray(ds2) #visualiza informações

