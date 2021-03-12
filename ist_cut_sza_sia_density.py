import numpy as np
import numpy.ma as ma
from pylab import *
import matplotlib.pyplot as plt
import os, sys, glob
from scipy import stats
from numpy.polynomial import polynomial as P

### SET VALUES ###
year = '2015'
month = ''
#ver = '#1'
#ver = '#2'
ver = '#3'
variables = [ 'IST_SIT' , 'IST_SZA', 'IST_TPW', 'IST_SIT_TPW', 'IST_SIT_SZA', 'IST_SZA_TPW', 'IST_SIT_SZA_TPW', 'IST_TPW_WSD' ]
var = variables[2]
#sza_cond = 'sza_ge70'
#sza_cond = 'sza_lt70'
print var

#######################################################

ist_cond = 'IST(Total)_SZA_SIA'
#ist_cond = 'IST(Cold)_SZA_SIA'
#ist_cond = 'IST(Medium)_SZA_SIA'
#ist_cond = 'IST(Warm)_SZA_SIA'

cbar_max = 300

ta_path  = '/home/eunkyung/polar_test/ta_polar/1.Data/1.Ta_ECMWF(ERA_Interim)/2.Validation_data/'
est_path = '/home/eunkyung/polar_test/ta_polar/2.Estimation/1.Ta/'+ver+'/'+var+'/'+ist_cond+'/'
day_path = '/home/eunkyung/polar_test/ta_polar/1.Data/'
fig_path = '/home/eunkyung/polar_test/ta_polar/0.Code/fig/ist_cut/'

#.................
nbins = 300 #??

#Graph axis min/max
#xmin = 0 ; xmax = 40    ###################
#ymin = -30 ; ymax = 30  ############
xmin = 230 ; xmax = 300    ###################
ymin = 230 ; ymax = 300  ############

#Graph statistical values position
xinter = 0.5 ; yinter = 3.0 #x/y inter = distance from x/y axis ###########################

ta_fn  = glob.glob(ta_path+'*'+year+month+'*.bin')
est_fn = glob.glob(est_path+'*'+year+month+'*.bin')
ta_fn.sort()
est_fn.sort()

flagx = 'ECMWF Ta'
flagy = 'Estimated Ta'

day = open(day_path+"list_day_validation.txt", "r")
day_cnt = day.readlines()

ta = [] ; est  = []

#for i in day_cnt :
for i in ta_fn :
  try:
    #ta_temp  = np.fromfile(ta_path+i[0:8]+'_1200_2m_temp.bin', dtype = float32)
    ta_temp  = np.fromfile(i, dtype = float32)
    print i[-25:-17]
    #est_temp = np.fromfile(est_path+'est_ta_'+var+'_'+i[0:8]+'.bin', dtype = float32)
    est_temp = np.fromfile(est_path+'est_ta_'+ver+'_'+var+'_'+i[-25:-17]+'.bin', dtype = float32)
    print est_path+'est_ta_'+ver+'_'+var+'_'+i[-25:-17]+'.bin'
  except IOError:
    print 'no file..: '+i
  else:
    ta.extend(ta_temp)
    est.extend(est_temp)

diff = np.array(diff)
ta   = np.array(ta)
est  = np.array(est)
print len(ta), len(est)

print 'finish reading files'

#Make Remove Index [ IST = not Fill Value, Not Ice(OISIC = FIll_Value) ]
indexRemove = np.where( np.logical_not( (ta != 0) & (ta > -50) & (est > 0) ) )

tot_diff = np.delete(diff, indexRemove)
tot_ta   = np.delete(ta, indexRemove)
tot_est  = np.delete(est, indexRemove)

tot_diff = np.subtract(tot_ta, tot_est)

tot_diff = np.array(tot_diff) ; tot_ta = np.array(tot_ta) ; tot_est = np.array(tot_est)
print 'Start histogram 2d'
print len(tot_diff), len(tot_ta), len(tot_est)

H, xedges, yedges = histogram2d(tot_ta, tot_est, bins=nbins) ###########################

H = rot90(H)
H = flipud(H)
Hmasked = np.ma.masked_where(H <= 50, H)

m, b = polyfit(tot_ta, tot_est, 1) ############################

m = round(m, 4)
b = round(b, 4)

resi = tot_ta - tot_est ############################
resi2 = resi * resi
rmse = round(sqrt(mean(resi2)), 4)
bias = round(mean(resi), 4)

grdi, iner, r_v, p_v, std = stats.linregress(tot_ta, tot_est) #########################

r2 = round(r_v ** 2, 4)

plot([xmin, xmax], [(xmin) * m + b, (xmax) * m + b], "r--")
plot([xmin, xmax], [ymin , ymax], "k-")

xlim(xmin, xmax) ; ylim(ymin, ymax)

xlabel(flagx + " (K)") ;  ylabel(flagy + " (K)") #########################

grid("on")

title('ECMWF Ta vs. Estimation Ta('+ver+')'+var+' ('+year+month+','+ist_cond+')') # + date_list[0] + ' ~ ' + date) ####################

text(xmin + xinter, ymax - yinter * 1, "R-square : " + str(r2), {'color': 'black', 'fontsize': 14})
text(xmin + xinter, ymax - yinter * 2, "RMS Diff : " + str(rmse), {'color': 'black', 'fontsize': 14})
text(xmin + xinter, ymax - yinter * 3, "Bias : " + str(bias), {'color': 'black', 'fontsize': 14})
text(xmin + xinter, ymax - yinter * 4, "Slope : " + str(round(m, 4)), {'color': 'black', 'fontsize': 14})
text(xmin + xinter, ymax - yinter * 5, "Intercept : " + str(round(b, 4)), {'color': 'black', 'fontsize': 14})
text(xmin + xinter, ymax - yinter * 6, "No. of points : " + str(len(tot_ta)), {'color': 'black', 'fontsize': 14})

print 'tot_est_mean'
print np.mean(tot_est)

pcolormesh(xedges, yedges, Hmasked, alpha=0.9, vmin=0, vmax=cbar_max) #, cmap='jet'
cbar = colorbar(extend="max")
cbar.ax.set_ylabel("count", fontsize=18)
grid("on")

savefig(fig_path+var+'_'+ver+'_'+year+month+'_'+ist_cond+'.png', dpi=300) ########################
plt.show()
close('all')

##### DIFF HISTOGRAM #####
fig = plt.figure(figsize=(12,10))
plt.title( 'ECMWF-Estimated Ta'+ist_cond, fontsize=24, fontweight='bold')
xmin=-30 ; xmax=30
ymin=0 ; ymax=50000

plt.hist( tot_diff, bins=200, range=(xmin,xmax) )

plot([0,0],[ymin,ymax],"r--")
axes = plt.gca()
axes.set_ylim([ymin,ymax])
axes.tick_params(labelsize=20) #axes parameter font size
axes.set_xlabel('Differences in Ta', fontsize=24)
axes.set_ylabel('Data counts', fontsize=24)
textstr='Mean bias: %.4f'%(np.mean(tot_diff))
grid("on")
print np.mean(tot_diff)
print tot_diff.min()
print tot_diff.max()
plt.text(-28, ymax-3000, textstr, {'color':'black','fontsize':24})

plt.show()
fig.savefig(fig_path+'histogram_DIFF_ta_'+var+'_'+ist_cond+'.png', dpi=300)





