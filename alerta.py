#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 12:44:00 2021

@author: felipe

Codigo para gerar o alerta com base nos arquivos NC de 5 dias do era5.
 - precipitacao (mm/h)
 - hs total (m) / sea + swell
 - magnitude do vento (m/s)

Esses arquivos já foram ajustados para a mesma grade (t, lat, lon).
Dados de hora em hora no período de 5 dias (120 horas) - 27/07/2020 00:00 a 31/07/2020 23:00

O alerta sera calculado em todos os pontos da grade, independente da area de interesse.


"""

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio
from scipy import interpolate



def find_idx(vetor, valor):
    # rotina para achar o indice do elemento do vetor mais proximo do valor
    dif = np.abs(vetor - valor)
    idx = np.where(dif == np.min(dif))[0][0]
    return idx



def save_nc(file,t,lat,lon,dado,var_name,data1):        
    # file = arquivo a ser gerado  
    # t = vetor de tempo
    # lat = vetor de latitude
    # lon = vetor de longitude    
    # dado = matriz com os dados [t, lat, lon]
    # var_name = nome da variavel para o NC
    # data1 = string com a data inicial e passo de tempo: 'hours since 2020-01-01'
    
    # abrindo o netCDF para escrita
    ncfile = nc.Dataset(file, 'w', format='NETCDF4')
    
    # Criando as dimensoes (que vao orientar o tamanho dos vetores e matrizes)
    [n_t,n_lat,n_lon] = dado.shape
    
    latitude_dim = ncfile.createDimension('latitude', n_lat)     # latitude axis
    longitude_dim = ncfile.createDimension('longitude', n_lon)    # longitude axis
    time_dim = ncfile.createDimension('time', n_t)  # None = unlimited axis (append)
    
    # Adicionando as variaveis em si e suas informacoes complementares
    latitude = ncfile.createVariable('latitude', np.float32, ('latitude',))
    latitude.units = 'degrees_north'
    latitude.long_name = 'latitude'
    latitude.standard_name = 'latitude'
    latitude.axis = 'Y'
    
    longitude = ncfile.createVariable('longitude', np.float32, ('longitude',))
    longitude.units = 'degrees_east'
    longitude.long_name = 'longitude'
    longitude.axis = 'X'
    longitude.standard_name = 'longitude'
    
    time = ncfile.createVariable('time', np.float64, ('time',))
    time.units = data1  # 'hours since 2020-01-01'
    time.long_name = 'time'
    
    # criando a variavel para nosso alerta
    # ela tera 3 dimensoes (tempo, lat, long).
    # Atencao a ordem deles pois sera importante na carga dos dados (ver linha 65)
    #
    dado_var = ncfile.createVariable(var_name, np.float32, ('time', 'latitude',
                                                          'longitude',))
    
    # Adicionando dados as variaveis criadas
    # Atencao pois o uso do '[:]' e obrigatorio, respeitando as dimensoes desejadas
    #
    latitude[:] = lat
    longitude[:] = lon
    time[:] = t
    
    dado_var[:,:,:] = dado
    
    # fechando o netcdf
    ncfile.close()





# lendo arquivo era5_202007_prec.nc ------------------------------------------
file1 = 'era5_202007_5d_prec.nc'
ds1 = nc.Dataset(file1)
# print(ds1)
# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF3_64BIT_OFFSET data model, file format NETCDF3):
#     Conventions: CF-1.6
#     history: 2021-03-26 21:32:39 GMT by grib_to_netcdf-2.16.0: /opt/ecmwf/eccodes/bin/grib_to_netcdf -S param -o /cache/data4/adaptor.mars.internal-1616794277.9518595-15365-15-aa3e2d42-037c-4d78-af52-4df33ec65802.nc /cache/tmp/aa3e2d42-037c-4d78-af52-4df33ec65802-adaptor.mars.internal-1616794277.952381-15365-6-tmp.grib
#     dimensions(sizes): longitude(9), latitude(9), time(744)
#     variables(dimensions): float32 longitude(longitude), float32 latitude(latitude), int32 time(time), int16 tp(time,latitude,longitude)
#     groups:

# carregando as coordenadas do .nc
lon1 = np.array(ds1['longitude'][:])
lat1 = np.array(ds1['latitude'][:])
# selecionando os indices do ponto de interesse
# idx_lat1 = find_idx(lat1,lat)
# idx_lon1 = find_idx(lon1,lon)
# carregando a serie temporal no ponto de interesse
dado_prec = np.array(ds1['prec'][:,:,:])  # passando pra mm/h





# lendo arquivo era5_202007_hs.nc --------------------------------------------
file2 = 'era5_202007_5d_hs.nc'
ds2 = nc.Dataset(file2)
# print(ds2)
# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF3_64BIT_OFFSET data model, file format NETCDF3):
#     Conventions: CF-1.6
#     history: 2021-03-26 21:36:37 GMT by grib_to_netcdf-2.16.0: /opt/ecmwf/eccodes/bin/grib_to_netcdf -S param -o /cache/data1/adaptor.mars.internal-1616794566.5306938-28215-3-ef35bf5b-ad70-4aaf-8572-d71a5282f23c.nc /cache/tmp/ef35bf5b-ad70-4aaf-8572-d71a5282f23c-adaptor.mars.internal-1616794566.531564-28215-1-tmp.grib
#     dimensions(sizes): longitude(5), latitude(5), time(744)
#     variables(dimensions): float32 longitude(longitude), float32 latitude(latitude), int32 time(time), int16 swh(time,latitude,longitude)
#     groups: 

# carregando as coordenadas do .nc
lon2 = np.array(ds2['longitude'][:])
lat2 = np.array(ds2['latitude'][:])
# selecionando os indices do ponto de interesse
# idx_lat2 = find_idx(lat2,lat)
# idx_lon2 = find_idx(lon2,lon)
# carregando a serie temporal no ponto de interesse
dado_hs = np.array(ds2['hs'][:,:,:])





# lendo arquivo era5_202007_wind.nc ------------------------------------------
file4 = 'era5_202007_5d_wind.nc'
ds4 = nc.Dataset(file4)
# print(ds4)
# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF3_64BIT_OFFSET data model, file format NETCDF3):
#     Conventions: CF-1.6
#     history: 2021-03-26 21:39:28 GMT by grib_to_netcdf-2.16.0: /opt/ecmwf/eccodes/bin/grib_to_netcdf -S param -o /cache/data5/adaptor.mars.internal-1616794703.5046206-21944-17-db0297df-1a0a-40d8-b575-cd5f603b73c5.nc /cache/tmp/db0297df-1a0a-40d8-b575-cd5f603b73c5-adaptor.mars.internal-1616794703.5051851-21944-8-tmp.grib
#     dimensions(sizes): longitude(9), latitude(9), time(744)
#     variables(dimensions): float32 longitude(longitude), float32 latitude(latitude), int32 time(time), int16 u10(time,latitude,longitude), int16 v10(time,latitude,longitude)
#     groups: 


# carregando as coordenadas do .nc
lon4 = np.array(ds4['longitude'][:])
lat4 = np.array(ds4['latitude'][:])
# selecionando os indices do ponto de interesse
# idx_lat4 = find_idx(lat4,lat)
# idx_lon4 = find_idx(lon4,lon)
# carregando a serie temporal no ponto de interesse
dado_wmag = np.array(ds4['wmag'][:,:,:])





# definindo os limites dos alertas parametricos
#  
# alerta 0  ->  x < param_1
# alerta 1  ->  param_1 <= x < param_2
# alerta 2  ->  x >= param_2


hs_1 = 1.5
hs_2 = 3

prec_1 = 2
prec_2 = 4

wmag_1 = 12
wmag_2 = 15



# criando a matriz com o alerta

[n_t, n_lat, n_lon] = dado_prec.shape
alerta = np.zeros((n_t, n_lat, n_lon))  # criando o alerta zerado


for i in range(n_t):  # analisando cada tempo
    
    # vamos comecar pelo alerta = 1
    # zerando indices
    idx_prec=[]
    idx_hs=[]
    idx_wmag=[]
    alerta1 = np.zeros((n_lat, n_lon))  # zerando a matriz alerta1 deste tempo
    
    
    # localizando indices onde as condicoes sao atendidas (alerta = 1)
    idx_prec = np.where(np.logical_and(dado_prec[i,:,:] > prec_1, dado_prec[i,:,:]<=prec_2))
    idx_hs = np.where(np.logical_and(dado_hs[i,:,:] > hs_1, dado_hs[i,:,:]<=hs_2))
    idx_wmag = np.where(np.logical_and(dado_wmag[i,:,:] > wmag_1, dado_wmag[i,:,:]<=wmag_2))
    
    # aplicando os valores do alerta1 neste tempo
    alerta1[idx_prec] = 1
    alerta1[idx_hs] = 1
    alerta1[idx_wmag] = 1
    


    # veremos o alerta 2 agora. Note que ele vai sobrescrever elementos do alerta 1 eventualmente.
    # zerando indices
    idx_prec=[]
    idx_hs=[]
    idx_wmag=[]
    alerta2 = alerta1  # aproveitando o alerta1
    
    # localizando indices onde as condicoes sao atendidas (alerta = 2)
    idx_prec = np.where(dado_prec[i,:,:] >= prec_2)
    idx_hs = np.where(dado_hs[i,:,:] >= hs_2)
    idx_wmag = np.where(dado_wmag[i,:,:] >= wmag_2)
    
    # aplicando os valores do alerta1 neste tempo
    alerta2[idx_prec] = 2
    alerta2[idx_hs] = 2
    alerta2[idx_wmag] = 2
    
    # aplicando o alerta na matriz final
    alerta[i,:,:] = alerta2  # aqui, temos os dois alertas






# # vamos salvar os NC do alerta

save_nc('alert_202007_5d.nc', np.arange(n_t), lat1, lon1, alerta,
        'alert', data1='hours since 2020-07-27')   

# save_nc('era5_202007_5d_hs.nc', np.arange(n_t), lat1, lon1, dado_hs,
#         'hs', data1='hours since 2020-07-26')   

# save_nc('era5_202007_5d_wind.nc', np.arange(n_t), lat1, lon1, dado_wmag,
#         'wmag', data1='hours since 2020-07-26')   

    
    
    











