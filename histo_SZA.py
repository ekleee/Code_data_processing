from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import os, sys, glob, re
#from statistics import stdev

data_path = '/home/eunkyung/polar_test/ta_polar/1.Data/8.SZA_Calc/'

sza_path = data_path

sza_fn = glob.glob(sza_path+'*.bin') 

sza_fn.sort()

nx = 304 ; ny = 448 ; FillValue=-999

sza = []

for d in sza_fn :
  sza_temp = np.fromfile(d, dtype=np.float32)
  sza.extend(sza_temp)


sza = array(sza)
indexRemove = np.where( np.logical_not((sza >= 0) ) )
tot_sza = np.delete(sza, indexRemove)

sza_bins = 100
sza_min = 0 ; sza_max = 180
ymin = 0 ; ymax = 50000

fig = plt.figure(figsize=(10,10))
fig.suptitle('Data histogram_SZA(20150701)', fontsize=16, fontweight='bold')

plt.hist( tot_sza, bins=sza_bins, range=(sza_min,sza_max) )
axes = plt.gca()
axes.set_ylim([ymin,ymax])
axes.set_xlabel('sza (K)')
axes.set_ylabel('Data counts')
plt.title( 'ECMWF sza', fontsize=12, fontweight='bold')
textstr='Standard daviation: %.2f'%(tot_sza.std())
textstr2='Total data counts: %i'%(len(tot_sza))
plt.text(sza_min+5, ymax-ymax/5, textstr, {'color':'black','fontsize':14})
plt.text(sza_min+5, ymax-ymax/15, textstr2, {'color':'black','fontsize':14})
fig.tight_layout() #fill figure.. on figure blank..
fig.subplots_adjust(hspace=0.3) #horizontal space between figures..
fig.subplots_adjust(top=0.93) #figure starting position (1(top)~0(bottom))


plt.show()


fig.savefig('DATA_HISTOGRAM_SZA', dpi=300)







