import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob, os

station = ['[Y01]', '[Y04]', '[Y06]']

ipath = 'C:/Users/jaemoo/Desktop/work/1.Data/3.Insitu/20170729-0806_Yeosu_ap-adom-asd_data/'
opath = 'C:/Users/jaemoo/Desktop/work/1.Data/3.Insitu/20170729-0806_Yeosu_ap-adom-asd_data/output/'

val = '1_(aw+aph)' #file name


fn = glob.glob(ipath+'*1_(aw+aph).txt')
fn.sort() #range files

for i in range(len(fn)):
    fn[i] = fn[i].replace(os.sep, '/')

flagx = 'Wavelength(um)'
flagy = '1/(aw+aph)'

xmin = 0 ; xmax=650 #xmax = number of x axis (wavelength range: 350~1000um => 650 columns)

#open, read coefficient file
'''
with open(i, "r") as f:
    content = f.readlines()
content = [x.strip() for x in content]
'''
#data = pd.read_csv(i, delimiter=' ')

print('=================================================================')

n=0
for i in fn :
    print(i)
    
    with open(i, "r") as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    
    #make list
    coe_a = []
    for j in range(len(data)):
        coe_a.append(float(data[j]))
    
    #make x axis (wavelength)
    wv = []
    for j in range(0, xmax+1, 100):
        wv.append(j)
    
    coe_a = np.array(coe_a)
    wv    = np.array(wv) #wavelength
    
    #make plot
    fig = plt.figure()
    #plt.plot(1,3,3)
    #plt.subplot(111)
    plt.figure(figsize=(7,4))
    plt.plot(coe_a, color='darkorange', linewidth=1.0, linestyle='-', label='1/(aw+aph)')
    plt.title(station[n]+' 1/(aw+aph)')
    plt.grid(color='lightgray')
    
    #axis setting
    plt.xticks(wv, ['350', '450', '550', '650', '750', '850', '950'])
    plt.xlabel(flagx)
    plt.ylabel(flagy)
    plt.xlim(xmin,xmax)
    plt.ylim(1.2*np.min(coe_a), 1.2*np.max(coe_a))
    
    #save and show
    plt.savefig(opath+station[n]+val+'png', dpi=300)
    #plt.show()
    
    n = n+1

print('end')
