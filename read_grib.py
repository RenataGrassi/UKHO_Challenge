#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 13:24:18 2021

@author: felipe
"""


# import xarray as xr
# from eccodes import *
import cfgrib
import matplotlib.pyplot as plt

#ds = xr.load_dataset('1mes.grib', engine='cfgrib')  # xarray
# print(ds)
# ds.t2m[0].plot(cmap=plt.cm.coolwarm)

# eccodes
#f = open('1mes.grib', 'rb')

#open a file
# ifile = open('1mes.grib', 'rb')
# while 1:
#     igrib = codes_grib_new_from_file(ifile)
#     if igrib is None: break
 
#     #Decode/encode data from the loaded message
#     date = codes_get(igrib,"dataDate")
#     levtype = codes_get(igrib,"typeOfLevel")
#     level = codes_get(igrib,"level")
#     values = codes_get_values(igrib)
#     print (date,levtype,level,values[0],values[len(values)-1])
 
#     #freed
#     codes_release(igrib)
# ifile.close()



# cfgrib
ds = cfgrib.open_file('1mes.grib')

