from pylab import *
import numpy as np
import numpy.ma as ma
import os, sys, glob, re
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std

##########REMOVE SIT CONDITION VERSION##########
data_path = '/home/eunkyung/polar_test/ta_polar/1.Data/'
t_folder = '/1.Training_data/'
n_folder = 'Normalized_data/'

sza_min = [] ; sza_max = []
#sia_min = [] ; sia_max = []
ist_min = [] ; ist_max = []

ist_min = [ 200, 265 ]
ist_max = [ 265, 330 ]

sza_min = [ 0, 90 ]
sza_max = [ 90, 180 ]

#sia_min = [ 0, 1, 2, 3, 4, 5 ]
#sia_max = [ 1, 2, 3, 4, 5, 16 ]

sza_fn = len(sza_min)
#sia_fn = len(sia_min)

ta_path = data_path+'1.Ta_ECMWF(ERA_Interim)'+t_folder
ist_path = data_path+'2.IST_MODIS'+t_folder
#sit_path = data_path+'3.SIT_APP-x'+t_folder
sit_path = data_path+'3.SIT_CryoSat-2'+t_folder
tpw_path = data_path+'4.TPW_MODIS'+t_folder+n_folder
sic_path = data_path+'5.SIC_OISST'+t_folder
sza_path = data_path+'8.SZA_Calc'+t_folder
#wsd_path = data_path+'10.WS_Calc'+t_folder
sia_path = data_path+'9.SIA'+t_folder

ta_fn  = glob.glob(ta_path+'*.bin') ; ta_fn.sort()
ist_fn = glob.glob(ist_path+'*.bin') ; ist_fn.sort()
#sit_fn = glob.glob(sit_path+'*.bin') ; sit_fn.sort()
tpw_fn = glob.glob(tpw_path+'*.bin') ; tpw_fn.sort()
sic_fn = glob.glob(sic_path+'*.bin') ; sic_fn.sort()
sza_fn = glob.glob(sza_path+'*.bin') ; sza_fn.sort()
#wsd_fn = glob.glob(wsd_path+'*.bin') ; wsd_fn.sort()
#sia_fn = glob.glob(sia_path+'*.bin') ; sia_fn.sort()

ta = [] ; ist = [] ; sit = [] ; tpw = [] ; sic = [] ; sza = [] ; tpw2 = [] # ; sia = [] ; wsd = []
#ta_temp = [] ; ist_temp = [] ; sit_temp = [] ; tpw_temp = [] ; sic_temp = [] ; sst_temp = [] ; sza_temp = []

day = open(data_path+"list_day_training.txt", "r")
day_cnt = day.readlines()
#day_cnt = day

f = open( 'Coefficient(IST,TPW,SZA_IST).txt', 'w')

for sza_n in range(0,len(sza_min)) :
  for ist_n in range(0,len(ist_min)) : 
    ta = [] ; ist = [] ; sit = [] ; tpw = [] ; sic = [] ; sza = [] ; tpw2 = []  # ; sia = [] ; wsd = []
    for d in day_cnt :
      #print d[0:8]
      ta_temp  = np.fromfile(ta_path+d[0:8]+'_1200_2m_temp.bin', dtype=np.float32)
      ist_temp = np.fromfile(ist_path+'MOD29E1D.A'+d[0:8]+'_IST_NP.bin', dtype=np.float32)
      tpw_temp = np.fromfile(tpw_path+'Normalized_MOD_Total_water_vapor_'+d[0:8]+'.bin', dtype=np.float32) #Normalized data
      #tpw_temp = np.fromfile(tpw_path+'MOD_Total_water_vapor_'+d[0:8]+'.bin', dtype=np.float32)
      sic_temp = np.fromfile(sic_path+'00OISIC_arctic_'+d[0:8]+'.bin', dtype=np.float32)
      #sza_temp = np.fromfile(sza_path+'MOD08_D3_Solar_Zenith_Mean_p'+d[0:8]+'.bin', dtype=np.float32)
      sza_temp = np.fromfile(sza_path+'Solar_zenith_arctic_calc_'+d[0:8]+'_12.bin', dtype=np.float32)
      #wsd_temp = np.fromfile(wsd_path+'ws_calc_'+d[0:8]+'.bin', dtype=np.float32)
      #sia_temp = np.fromfile(sia_path+'cov_iceage.grid.day.'+d[0:8]+'.n.v3.bin', dtype=np.float32)

      ta.extend(ta_temp)
      ist.extend(ist_temp)
      tpw.extend(tpw_temp)
      sic.extend(sic_temp)
      sza.extend(sza_temp)
      #wsd.extend(wsd_temp)
      #sia.extend(sia_temp)
    
    print len(ta), len(ist), len(sza), len(tpw)#, len(wsd)

    ta = array(ta) ; ist = array(ist) ; sza = array(sza) ; tpw = array(tpw) ; sic = array(sic) # ; sia= array(sia) ; wsd = array(wsd)

    #print 'ta' , ta.min(),  ta.max()
    #print 'ist', ist.min(), ist.max()
    #print 'tpw', tpw.min(), tpw.max()
    #indexRemove = np.where( np.logical_not( (ta > 0) & (ist > 0) & (ist < ist_min) & (sic > 0.15) & (tpw >= 0) & (sza >= sza_min[sza_n]) & (sza < sza_max[sza_n]) & (sia > sia_min[sia_n]) & (sia <= sia_max[sia_n]) ) ) 
    indexRemove = np.where( np.logical_not( (ta > 0) & (ist > 0) & (sic > 0.15) & (tpw >= 0) & \
    (sza >= sza_min[sza_n]) & (sza < sza_max[sza_n]) & (ist > ist_min[ist_n]) & (ist <= ist_max[ist_n]) ) ) 
    tot_ta  = np.delete(ta, indexRemove)
    tot_ist = np.delete(ist, indexRemove)
    tot_sza = np.delete(sza, indexRemove)
    tot_tpw = np.delete(tpw, indexRemove)
    
    #tot_sia = np.delete(sia, indexRemove)
    #tot_wsd = np.delete(wsd, indexRemove)
    #tot_sic = np.delete(sic, indexRemove)
    print len(tot_ta), len(tot_ist), len(tot_sza), len(tot_tpw) #, len(tot_sia), len(tot_wsd)
    '''
    if len(tot_ta) <= 100 :
      continue
    '''
    if sza_n == 0 :
      x = sm.add_constant( zip(tot_ist, tot_tpw, tot_sza), prepend=True )
      result = sm.OLS(tot_ta, x).fit()
      print ''
      print '['+str(sza_min[sza_n])+'<=sza<'+str(sza_max[sza_n])+']'+','+'['+str(ist_min[ist_n])+'<ist<='+str(ist_max[ist_n])+']'
      cond='['+str(sza_min[sza_n])+'<=sza<'+str(sza_max[sza_n])+']'+','+'['+str(ist_min[ist_n])+'<ist<='+str(ist_max[ist_n])+']'
      print result.summary()

      const = result.params[0]
      ist_coe = result.params[1]
      #tpw_coe = result.params[2]
      tpw_coe = result.params[2]
      sza_coe = result.params[3]

      print 'tot_ta', tot_ta.min(), tot_ta.max()
      print 'tot_tpw', tot_tpw.min(), tot_tpw.max()
      print 'tot_ist', tot_ist.min(), tot_ist.max()
      print 'tot_sza', tot_sza.min(), tot_sza.max()
      print '========================================='
      line = cond+'  '+str(const)+'  '+str(ist_coe)+'  '+str(tpw_coe)+'  '+str(sza_coe)+'\n'
      f.write(line)

    else:
      x = sm.add_constant( zip(tot_ist, tot_tpw), prepend=True )
      result = sm.OLS(tot_ta, x).fit()
      print ''
      print '['+str(sza_min[sza_n])+'<=sza<'+str(sza_max[sza_n])+']'+','+'['+str(ist_min[ist_n])+'<ist<='+str(ist_max[ist_n])+']'
      cond='['+str(sza_min[sza_n])+'<=sza<'+str(sza_max[sza_n])+']'+','+'['+str(ist_min[ist_n])+'<ist<='+str(ist_max[ist_n])+']'
      print result.summary()

      const = result.params[0]
      ist_coe = result.params[1]
      #tpw_coe = result.params[2]
      tpw_coe = result.params[2]

      print 'tot_ta', tot_ta.min(), tot_ta.max()
      print 'tot_tpw', tot_tpw.min(), tot_tpw.max()
      print 'tot_ist', tot_ist.min(), tot_ist.max()
      print 'tot_sza', tot_sza.min(), tot_sza.max()
      print '========================================='
      line = cond+'  '+str(const)+'  '+str(ist_coe)+'  '+str(tpw_coe)+'\n'
      f.write(line)

f.close()
print 'finish'
'''
fig = plt.figure(figsize=(10,10))
plt.hist(tot_ta, bins=200, range=(230,300) )
fig.savefig('histogram_ecmwf_ta.png', dpi=300)
close('all')
fig = plt.figure(figsize=(10,10))
plt.hist(tot_tpw, bins=200, range=(0,5) )
fig.savefig('histogram_tpw.png', dpi=300)
close('all')
fig = plt.figure(figsize=(10,10))
plt.hist(tot_ist, bins=200, range=(230,300) )
fig.savefig('histogram_ist.png', dpi=300)
close('all')
'''
