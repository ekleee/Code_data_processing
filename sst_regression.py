from pylab import *
from numpy import *

import scipy.stats as stats
import statsmodels.api as sm

F=open("Results(day)_Training.txt","r")
raw=F.readlines()
F.close()

data=[]
for d in raw:
  data.append( [float(i) for i in d.strip().split()] )
data=array(data)

buoy = data[:,17]

VZA  = radians(data[:,16])
in1  = data[:,13]
in2  = data[:,13]-data[:,14]
in3  = in2*((1/cos(VZA))-1)


x    = sm.add_constant( zip(in1,in2,in3), prepend=True )

result = sm.OLS( buoy, x).fit()

print result.summary()

#calculated COMS SST coefficients
#day   :  0.9975 , 2.5848 , 0.3122 , -1.5366
#night :  0.9930 , 2.4880 , 0.3390 , -0.4139

#correction TBB 
#day   :  0.9862 , 2.5283 , 0.4224 , 0.9105
#night :  0.9817 , 2.4274 , 0.4640 , 1.9631

'''
daytime
sst = 0.985098*in1 + 2.338343*in2 + 0.545135*in3 -0.321399
night
sst = 0.975640*in1 + 2.496965*in2 + 0.353631*in3 -0.031189
'''
