#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 22:49:02 2021

Programa para gerar um netcdf contendo nosso alerta

A ideia e gerar uma grade pequena de lat x lon e gerar um campo que varie
no tempo (2 ou 3 dias).

A priori, falamos em usar os seguintes valores para o alerta:

    0 = normalidade
    1 = Atencao
    2 = crítico


@author: felipe

"""

import numpy as np
import netCDF4 as nc

# arquivo a ser gerado
file = 'test2.nc'

# abrindo o netCDF para escrita
ncfile = nc.Dataset(file, 'w', format='NETCDF4')

# Criando as dimensoes (que vao orientar o tamanho dos vetores e matrizes)
latitude_dim = ncfile.createDimension('latitude', 2)     # latitude axis
longitude_dim = ncfile.createDimension('longitude', 2)    # longitude axis
time_dim = ncfile.createDimension('time', 4)  # None = unlimited axis (append)

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
time.units = 'hours since 2020-01-01'
time.long_name = 'time'

# criando a variavel para nosso alerta
# ela tera 3 dimensoes (tempo, lat, long).
# Atencao a ordem deles pois sera importante na carga dos dados (ver linha 65)
#
alerta = ncfile.createVariable('alerta', np.float32, ('time', 'latitude',
                                                      'longitude',))

# Adicionando dados as variaveis criadas
# Atencao pois o uso do '[:]' e obrigatorio, respeitando as dimensoes desejadas
#
latitude[:] = np.arange(18.0, 18.6, 0.5)
longitude[:] = np.arange(-63.5, -62.9, 0.5)
time[:] = [0, 1, 2, 3]

# criando um alerta fake, variando no tempo e em apenas um ponto.
# tempo 1
alerta[0, 0, 0] = 0
alerta[0, 1, 0] = 0
alerta[0, 0, 1] = 0
alerta[0, 1, 1] = 0
# tempo 2
alerta[1, 0, 0] = 0
alerta[1, 1, 0] = 0
alerta[1, 0, 1] = 1
alerta[1, 1, 1] = 0
# tempo 3
alerta[2, 0, 0] = 0
alerta[2, 1, 0] = 0
alerta[2, 0, 1] = 1
alerta[2, 1, 1] = 0
# tempo 4
alerta[3, 0, 0] = 0
alerta[3, 1, 0] = 0
alerta[3, 0, 1] = 2
alerta[3, 1, 1] = 0

# fechando o netcdf
ncfile.close()
