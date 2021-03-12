from mpl_toolkits.basemap import Basemap, cm
from pylab import*
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import os, sys, glob, re

ipath = '/home/eunkyung/polar_test/ta_polar/2.Estimation/1.Ta/#3/IST_TPW/IST(Total)_SZA_SIA/Average/'
opath = '/home/eunkyung/polar_test/ta_polar/0.Code/fig/Est_Ta/'


#fn=glob.glob(ipath+'*.bin')
#fn=glob.glob(ipath+'*allDate*.bin')

fn=glob.glob(ipath+'*201509*.bin')
vmin=250 ; vmax=280

fn.sort()
for i in fn :
   # if i[42:44] != '15': 
   #     continue
    sic = np.fromfile(i,dtype=np.float32).reshape(448,304)
    sic = ma.masked_where(sic == -999,sic )
    var = i[-22:-11]
    plt.figure(figsize=(8,9.5))
    m = Basemap(projection='stere',resolution='l',lat_0=90,lon_0=-45, lat_ts=70,\
#                llcrnrlon = 279.95,urcrnrlon=101.65,llcrnrlat=34.91,urcrnrlat=31.2)
               llcrnrlon = 279.31,urcrnrlon=103.4,llcrnrlat=34.7,urcrnrlat=32.3)
    m.imshow(sic,interpolation='nearest', origin='upper',cmap=cm.get_cmap('jet'), vmin=vmin, vmax=vmax)
    cbar = m.colorbar(extend='both', size="5%", pad=0.05)
    cbar.set_label('Estimated air temperature(Ta)')
    plt.title('Estimated Ta '+'('+i[-10:-4]+')', fontsize=14)
    m.drawcoastlines()
    m.fillcontinents()
    m.drawparallels(np.arange(-90.,120.,15.),labels=[1,0,0,0],fontsize=10)
    m.drawmeridians(np.arange(0.,420.,15.),labels=[0,0,0,1],fontsize=10)
#    m.drawmapboundary()
#    m.imshow(sic,interpolation='nearest', origin='upper',cmap=cm.get_cmap('jet'), vmin=251,  vmax=255)
    savefig(opath+var+'_'+i[-10:-4]+'.png',dpi=300)
    print var+'_'+i[-10:-4]
    close('all')
    plt.show()


