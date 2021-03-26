#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:08:28 2021

Programa para ler arquivos netCDF da reanalise ERA5

Temos arquivos de hora em hora para jul/2020 com os seguintes parametros:
    - precipitacao total (m)
    - Hs (m)
    - mslp (pressao no nivel medio do mar - Pa)
    - vento (u10 e v10)

@author: felipe
"""
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio



def find_idx(vetor, valor):
    # rotina para achar o indice do elemento do vetor mais proximo do valor
    dif = np.abs(vetor - valor)
    idx = np.where(dif == np.min(dif))[0][0]
    return idx



# coordenadas do ponto de interesse
lat = 17.5
lon = -63    



# lendo arquivo era5_202007_prec.nc ------------------------------------------
file1 = 'era5_202007_prec.nc'
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
idx_lat1 = find_idx(lat1,lat)
idx_lon1 = find_idx(lon1,lon)
# carregando a serie temporal no ponto de interesse
dado_prec = np.array(ds1['tp'][:,idx_lat1,idx_lon1])*1000  # passando pra mm/h





# lendo arquivo era5_202007_hs.nc --------------------------------------------
file2 = 'era5_202007_hs.nc'
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
idx_lat2 = find_idx(lat2,lat)
idx_lon2 = find_idx(lon2,lon)
# carregando a serie temporal no ponto de interesse
dado_hs = np.array(ds2['swh'][:,idx_lat2,idx_lon2])






# lendo arquivo era5_202007_mslp.nc ------------------------------------------
file3 = 'era5_202007_mslp.nc'
ds3 = nc.Dataset(file3)
# print(ds3)
# <class 'netCDF4._netCDF4.Dataset'>
# root group (NETCDF3_64BIT_OFFSET data model, file format NETCDF3):
#     Conventions: CF-1.6
#     history: 2021-03-26 21:39:07 GMT by grib_to_netcdf-2.16.0: /opt/ecmwf/eccodes/bin/grib_to_netcdf -S param -o /cache/data3/adaptor.mars.internal-1616794686.2464159-27236-29-20a976a7-3ad1-4781-bd59-28d0cb317e9f.nc /cache/tmp/20a976a7-3ad1-4781-bd59-28d0cb317e9f-adaptor.mars.internal-1616794686.2469478-27236-9-tmp.grib
#     dimensions(sizes): longitude(9), latitude(9), time(744)
#     variables(dimensions): float32 longitude(longitude), float32 latitude(latitude), int32 time(time), int16 msl(time,latitude,longitude)
#     groups: 

# carregando as coordenadas do .nc
lon3 = np.array(ds3['longitude'][:])
lat3 = np.array(ds3['latitude'][:])
# selecionando os indices do ponto de interesse
idx_lat3 = find_idx(lat3,lat)
idx_lon3 = find_idx(lon3,lon)
# carregando a serie temporal no ponto de interesse
dado_msl = np.array(ds3['msl'][:,idx_lat3,idx_lon3])/100  # convertendo pra hPa




# lendo arquivo era5_202007_wind.nc ------------------------------------------
file4 = 'era5_202007_wind.nc'
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
idx_lat4 = find_idx(lat4,lat)
idx_lon4 = find_idx(lon4,lon)
# carregando a serie temporal no ponto de interesse
dado_u10 = np.array(ds4['u10'][:,idx_lat4,idx_lon4])
dado_v10 = np.array(ds4['u10'][:,idx_lat4,idx_lon4])
dado_wmag = np.array(np.sqrt(np.multiply(dado_u10,dado_u10) + np.multiply(dado_v10,dado_v10)))  # magnitude do vento



# Plots - serie completa

fig = plt.figure()
plt.title('Magnitude do vento')
plt.plot(dado_wmag)
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('Vento (m/s)')
plt.ylim([0, 20])
fig.set_size_inches(13,4)
plt.savefig('fig_wmag.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

fig = plt.figure()
plt.title('Precipitação total')
plt.plot(dado_prec)
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('(mm/h)')
plt.ylim([0, 8])
fig.set_size_inches(13,4)
plt.savefig('fig_prec.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

fig = plt.figure()
plt.title('Altura significativa de onda')
plt.plot(dado_hs)
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('(m)')
plt.ylim([0, 6])
fig.set_size_inches(13,4)
plt.savefig('fig_hs.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

fig = plt.figure()
plt.title('Pressao ao nivel do mar')
plt.plot(dado_msl)
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('(hPa)')
plt.ylim([1005, 1025])
fig.set_size_inches(13,4)
plt.savefig('fig_pressao.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()











# Plots - intervalo

x1 = 620
x2 = 744

fig = plt.figure()
plt.title('Magnitude do vento')
plt.plot(np.arange(x1-1,x2), dado_wmag[x1-1:])
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('Vento (m/s)')
plt.ylim([0, 20])
fig.set_size_inches(13,4)
plt.savefig('fig_intervalo_wmag.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

fig = plt.figure()
plt.title('Precipitação total')
plt.plot(np.arange(x1-1,x2), dado_prec[x1-1:])
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('(mm/h)')
plt.ylim([0, 8])
fig.set_size_inches(13,4)
plt.savefig('fig_intervalo_prec.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

fig = plt.figure()
plt.title('Altura significativa de onda')
plt.plot(np.arange(x1-1,x2), dado_hs[x1-1:])
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('(m)')
plt.ylim([0, 6])
fig.set_size_inches(13,4)
plt.savefig('fig_intervalo_hs.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

fig = plt.figure()
plt.title('Pressao ao nivel do mar')
plt.plot(np.arange(x1-1,x2), dado_msl[x1-1:])
plt.grid()
plt.xlabel('t (h)')
plt.ylabel('(hPa)')
plt.ylim([1005, 1025])
fig.set_size_inches(13,4)
plt.savefig('fig_intervalo_pressao.jpg', dpi=200, bbox_inches='tight', pad_inches=0.1)
plt.show()
plt.close()

# exportando para .mat

# out = dict()
# out['wmag'] = out_wmag
# out['u10'] = out_u10
# out['v10'] = out_v10
# out['msl'] = out_msl
# out['tp'] = out_tp
# out['shww'] = out_shww
# out['shts'] = out_shts

# scio.savemat('era5_track.mat', out) 








