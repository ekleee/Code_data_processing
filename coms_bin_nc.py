from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, cm
from pylab import*
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import numpy.ma as ma
import os, sys, glob, re


#ri=Rainfall Intensity, coms_mi_le2p_ri_cn_201510010000.nc
#ll=ri Lat Lon file = coms_cn_latlon.nc
#pe=Precipitation Estimates, CMORPH_V1.0_ADJ_8km-30min_2015070100
ri_path = '/data/ECVs/RI/L2P_RI/results_2gsics/Y2015/'
ll_path = '/data/ECVs/RI/L2P_RI/'
pe_path = '/ecoface/EKLEE/ncbin_1019/CMORPH/'

file_date = np.array['20150701', '20150710', '20151001']
hour = np.array['00', '12']

#SET cmap
fig = plt.figure(figsize=(20,15))
cmap=cm.get_cmap('jet', 16)


#---RI LATLON FILE ---
fl = Dataset(ll_path+'coms_cn_latlon.nc', mode='r') #r=only read mode
rlon = fl.variables['lon'][:,:]
rlat = fl.variables['lat'][:,:]

rlon_len = len(rlon) ; rlat_len = len(rlat)
rlon_0 = min(rlon) ; rlat_0 = min(rlat)
rlon_1 = max(rlon) ; rlat_1 = max(rlat)
#---------------------

#---PE LATLON---
#X(4948): min=0.036378335/interval=0.072756669, Y(1649): min=-59.963614/interval=0.072771377
plon_len = 1649 ; plat_len = 4948
plon_0 = 0.036378335 ; plat_0 = -59.963614
plon_1 = 359.999998212  ; plat_1 = 60.036386673
#-----------------------------------------------------


n=0

for i in file_date :
    for hh in hour :
        n=n+1
        #---RI FILE SUBPLOT---
#        plt.subplot(6,2,n) #subplot(y,x,position)
        plt.subplot(6,1,n) #subplot(y,x,position)

        #---READ RI FILE---NC FILE!
        fn_name = 'coms_mi_le2p_ri_cn_'+i+hh+'00.nc'
        fn = Dataset(ri_path+i+'/'+fn_name, mode='r') #r=only read mode
        rain_ins = fn.variables['Rainfall_Intensity'][:]

        array = np.empty((rlat_len,rlon_len))
        array[:] = rain_ins[:]
        print 'file::::: '+fn_name

        #---RI FILE MAP---
        array = ma.masked_where(array == -99999., array) #criteria array = ma.masked_where(array=range, applying array)

        m = Basemap(projection='cyl', llcrnrlat=rlat_0, urcrnrlat=rlat_1, llcrnrlon=rlon_0, urcrnrlon=rlon_1, resolution='c')
        m.drawcoastlines()
        m.drawparallels(np.arange(-10,60,20), labels=[1,0,0,0], fontsize=9) #labels=[left,right,top,bottom] #horizontal line
        m.drawmeridians(np.arange(80,180,20), labels=[0,0,0,1], fontsize=9) #labels=[left,right,top,bottom] #vertical line

        m.imshow(array, cmap=cmap, vmin=0, vmax=100) #draw figure
        plt.title(fn_name, fontsize=9)

        cbar = m.colorbar(size="5%", pad=0.05, extend='max') #pad=distance, extend='colorbar shape,,'
        cbar.ax.tick_params(labelsize=8) #labelsize=colorbar font size
        cbar.set_label('Rainfall intensity(mm/hr)', fontsize=8, ha='center') #ha='label text position'
        #------------------
'''
        n=n+1

        #---PE FILE SUBPLOT---
        plt.subplot(6,2,n) #subplot(y,x,position)

        #---READ PE FILE---BINARY FILE!
        fb_name = 'CMORPH_V1.0_ADJ_8km-30min_'+i+hh
        pe = np.fromfile(pe_path+fb_name, dtype=np.float64).reshape(1649,4948)

        #---PE FILE MAP---
        pe = ma.masked_where(pe == -999, pe)
        n = Basemap(
        m.imshow(pe, cmap=cmap, vmin=0, vmax=100) #draw figure
        cbar = m.colorbar(size="5%", pad=0.05, extend='max') #pad=distance, extend='colorbar shape,,'
        cbar.ax.tick_params(labelsize=8) #labelsize=colorbar font size
        cbar.set_label('Precipitation extimates(mm/hr)', fontsize=8, ha='center')

        #SET FIGURE
        fig.tight_layout() #fill figure.. on figure blank..
        fig.subplots_adjust(hspace=0.3) #horizontal space between figures..
        fig.subplots_adjust(top=0.93) #figure starting position (1(top)~0(bottom))
'''
#        n=n+1
#    k=k+1

plt.show()
fig.savefig('prec_inte.png', dpi=300)

fn.close()



