import numpy as np
import math
import numpy.ma as ma
from pylab import*
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import os, sys, glob
from scipy import stats
from scipy.stats import gaussian_kde

o_path='/home/darae/landsat/density/'
pname=['enp', 'sdg']

be_total2=[] ; af_total2=[]

win=3
ext=win/2.
#ext = 1

for nn in range(len(pname)):
  L8_path='/home/darae/landsat/albedo_high_v4_1/'+pname[nn]+'/mask/'
  L7_path='/home/darae/landsat/albedo_high_v4_1/'+pname[nn]+'/mask/'

  fn = glob.glob(L8_path+'8*.bin')
  fn.sort()
  ft = glob.glob(L7_path+'7*.bin')
  ft.sort()

  if nn == 0 :
    nx = 291
    ny = 321
  else :
    nx = 215
    ny = 178

  for i in range(len(fn)):
    name=os.path.basename(fn[i])
    nn=name[1:4]
    date=name[5:13]

    print date, nn

    af_ndvi=np.fromfile(fn[i], dtype=np.float32).reshape((ny, nx))
    be_ndvi=np.fromfile(ft[i], dtype=np.float32).reshape((ny, nx))

    af_ndvi[(af_ndvi <= 0) |(be_ndvi <= 0)] = np.NaN
    be_ndvi[(af_ndvi <= 0) |(be_ndvi <= 0)] = np.NaN

    for k in arange(0+ext,ny-ext,1):
      for j in arange(0+ext, nx-ext,1):
          if be_ndvi[k,j] != NaN :
	     be33 = be_ndvi[k-ext:k+ext, j-ext:j+ext]
             af33 = af_ndvi[k-ext:k+ext, j-ext:j+ext]
             be_total2.append(mean(be33))
             af_total2.append(mean(af33))
          else:
             contiune
        
be_total2 = np.array(be_total2)
af_total2 = np.array(af_total2)

be_total = be_total2[~np.isnan(be_total2)&~np.isnan(af_total2)]
af_total = af_total2[~np.isnan(be_total2)&~np.isnan(af_total2)]

fig = plt.figure(figsize=(10,10))

# Min, Max
xmin  =  0. ; xmax  = 0.5 ; xinter =  0.1
ymin  =  0. ; ymax  = 0.5 ; yinter =  0.1

slop, inter, r_v, p_v, std = stats.linregress(be_total,af_total)

slop  = round(slop, 4)
inter = round(inter, 4)

resi  = af_total - be_total
resi2 = resi*resi
rmse  = round(sqrt(mean(resi2)),4)
bias  = round(mean(resi),4)
r2    = round( r_v**2,4)

print slop, inter
print rmse, bias

plot([xmin,xmax],[(xmin)*slop+inter,(xmax)*slop+inter],"r--")
plot([xmin, xmax], [xmin, xmax], "k-", lw=0.5)

xran = arange (xmin, xmax, xinter)+0.1
yran = arange (ymin, ymax, yinter)+0.1

xticks ( xran, [float(j) for j in xran], fontsize=20 )
yticks ( yran, [float(k) for k in yran], fontsize=20 )
xlim(0,0.5)
ylim(0,0.5)

xlabel("Landsat-7 Albedo", {'fontsize':20})
ylabel("Landsat-8 Albedo", {'fontsize':20})

title(" Landsat-7 vs Landsat-8 \n", {'fontsize':20})
#text( -1, 38, "(a)", {'color':'black','fontsize':25})t
text( 0.02, 0.48, "R-square : "+ str(r2),{'color':'black','fontsize':20})
text( 0.02, 0.46, "RMS Diff : "+ str(rmse),{'color':'black','fontsize':20})
text( 0.02, 0.44, "Bias : "+ str(bias),{'color':'black','fontsize':20})
text( 0.02, 0.42, "Slope : "+ str(slop),{'color':'black','fontsize':20})
text( 0.02, 0.40, "Intercept : "+ str(inter),{'color':'black','fontsize':20})
text( 0.02, 0.38, "No. of points : "+ str(len(be_total)),{'color':'black','fontsize':20})

nbins = 300
H, xedges, yedges = np.histogram2d(be_total,af_total, bins = nbins)
H = np.rot90(H)
H = np.flipud(H)
Hmasked = np.ma.masked_where(H<=1, H)

pcolormesh(xedges, yedges, Hmasked, alpha = 0.9, vmin = 0, vmax =50)
cbar = colorbar(extend="max")
cbar.ax.set_ylabel("count",fontsize=20)
cbar.ax.tick_params(labelsize=20)
grid("on")
xlim(0,0.5) ; ylim(0,0.5)
savefig(o_path+'density_all_day.png',dpi=250)
plt.show()
plt.close()

