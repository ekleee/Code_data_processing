import numpy as np
from scipy import ndimage
from pylab import*
import numpy.ma as ma
import glob, sys

def block_mean(ar, fact):
    assert isinstance(fact, int), type(fact)
    sx, sy = ar.shape
    X, Y = np.ogrid[0:sx, 0:sy]
    regions = sy/fact * (X/fact) + Y/fact
    res = ndimage.mean(ar, labels=regions, index=np.arange(regions.max() + 1))
    res.shape = (sx/fact, sy/fact)
    return res

path = '/mnt/hgfs/KOPRI_CryosphereStudy/DATA/Sea_Ice/SIC/2.SIC_data/'
fi = glob.glob(path+'/1.bin/SIC_bin/*.SIC')
fi.sort()

#ff = glob.glob(path+'/1.bin/flag/*.SIC')
#ff.sort()

for i in range(len(fi)):
    ar = np.fromfile(fi[i], dtype= np.int16).reshape(849,849)
#    mask = np.fromfile(ff[i], dtype=np.int8).reshape(849,849)
#    ar = ma.masked_where(mask != 0 , ar)
    ar2 = ar[1:849, 1:849]

    k = block_mean(ar2, 2)
    k = k.astype(np.float32)
    
    name = fi[i]
 
    f = open(path+'/2.congrid/con_'+name[-16:-4]+'.SIC', 'w')
    f.write(k)
    f.close()
    close('all')
    print name[-16:-4]






