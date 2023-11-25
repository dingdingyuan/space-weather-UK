#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:08:40 2022

@author: yuanding
"""

# Parameters
#  Figure 2
# Love, J. J. (2021). Dst intensities for solar cycles 14–24. Space Weather, 19, e2020SW002579. 
# https://doi.org/10.1029/2020SW002579
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from PIL import ImageColor

Weibull = False # W 
GEV =  False  # T
Gumbel = True  # G
solar_cycle=11.

"""
if Weibull: # W
    mu = 402.528 #  nT
    sigma = 129.885 # nT
    xi = -0.062
    zero_xi = False
    
if Gumbel: # G
    mu = 400.757 # nT
    sigma = 128.406 # nT
    xi = 0
    zero_xi = True
    
if GEV: # T
    mu= 401.295 # nT 
    sigma = 128.647 # nT
    xi=-0.018
    zero_xi = False
"""
    
#  Eq. 32 
#  Verification with Sec. 15
# -Dst for a 1 in 100 years event with Weibull model 
cTao_nz = 1./9. # 1 of nine solar cycles. \bar{Tao} 


if Weibull:
    mu = 402.528 #  nT
    sigma = 129.885 # nT
    xi = -0.062
    zero_xi = False
    quantile_x_W = mu+sigma/xi*((-math.log(1-cTao_nz))**(-xi) -1)
#%%
Gumbel = True
if Gumbel:
    mu = 400.757 # nT
    sigma = 128.406 # nT
    xi = 0
    zero_xi = True
    # Check with value pair in Figure 2: 500 nT, cTao=0.38 for G1
    cTao_nz = 0.38
    quantile_x_G = mu-sigma*math.log(-math.log(1-cTao_nz))
    T_scales=np.array([11.01, 22, 33, 55, 110, 1000, 10000, 100000, 1000000])/solar_cycle #  Unit in solar cycle
    N_scales= len(T_scales)
    cTao_scales = 1/T_scales #  number per solar cycle 
    Dst_scales = mu-sigma*np.log(-np.log(1.-cTao_scales)) #  Eq. 18 
    
    disaster_in_str = ['1-in-11','1-in-22','1-in-33', \
                       '1-in-55','1-in-110','1-in-1 000', \
                       '1-in-10 000','1-in-100 000','1-in-1 000 000']
      

    
    #event_scale= 1./(T_int) #  number per solar cycle 
    #quantile_x_G_list = mu-sigma*np.log(-np.log(1.-event_scale)) #  Eq. 18 
    
    ##  
    
    cTao_grid = np.logspace(-8,0,num=81,base=10.0,endpoint=True) # number per solar cycle 
    cTao_grid[-1] -= 0.001 # shift from 1.0 to avoid Inf in numerical calculation 
    Dst_grid = mu-sigma*np.log(-np.log(1.-cTao_grid)) #  Eq. 18 
    
    
    
    
    #test
    a = 2200
    T_x = a/solar_cycle
    event_scale_x = 1. / T_x
    xi = -0.018
    x1 = mu - sigma * np.log(-np.log(1. - event_scale_x))
    x2 = mu + sigma / xi * ((-np.log(1 - event_scale_x)) ** (-xi) - 1)
    print(x1)
    print(x2)
    
    #a = np.append(np.arange(0.01, 100.01, 0.1), np.arange(100.01, 100000000.01, 10))
    #T_x = a/solar_cycle
   # event_scale_x = 1. / T_x # byn
   # y = np.log10(event_scale_x)
   # x = mu - sigma * np.log(-np.log(1. - event_scale_x))
    
    

    plt.rcParams["figure.figsize"] = (8,6)
    #fig, ax= plt.figure(figsize=(8, 6), dpi=600)  
    
    plt.plot(Dst_grid, cTao_grid, 'r', linewidth=3,alpha=0.5)
    
    
    areas = 50*np.log(T_scales)
    colors = ["black","#999999","#666666","#80FF00","#00FF80","#FFD700","#FF8000","brown","#FF0000"]
    plt.scatter(Dst_scales, cTao_scales, s=areas, c=colors, alpha=0.5)
    

    x0,x1 = 0,2500 #  plot range 0, 2500 nT
    y0,y1 = 1e-8,10
    el = mpatches.Ellipse((x1, y1), 0.3, 0.4, angle=30, alpha=0.2)
    
    x_off = [600, 300, 220,\
             800,700,410,\
              600,300,5 ]
    y_off = [2, 0.5, 0.0, \
             0.8,0.18,0.07, \
              0.01,0.003,0.001] 
    
    

    for k in range(N_scales):
      
      plt.plot([Dst_scales[k],Dst_scales[k]],[cTao_scales[k],y0],linestyle='dashdot',linewidth=2,color='grey',alpha=0.5)
      plt.plot([x0,Dst_scales[k]],[cTao_scales[k],cTao_scales[k]],linestyle='dashdot',linewidth=2,color='grey',alpha=0.5)
      
      plt.annotate(disaster_in_str[k], xy=(Dst_scales[k], cTao_scales[k]), \
                   xytext=(Dst_scales[k]+x_off[k], cTao_scales[k]+y_off[k]), 
                   xycoords='data', fontsize=15,\
                  horizontalalignment='left',verticalalignment='bottom',\
                   arrowprops=dict(arrowstyle="fancy",color="0.5",alpha=0.3,\
                                   patchB=el,shrinkB=5,connectionstyle="arc3,rad=0.3")
                     )
    #'family': 'Arial',
    style_list = ['default', 'classic', 'Solarize_Light2', 'bmh', 'dark_background', 'fast', 'fivethirtyeight',
                  'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark',
                  'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook',
                  'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white',
                  'seaborn-whitegrid', 'tableau-colorblind10']
    for i in style_list:
        plt.style.use(i)
        if i == 'bmh':
            break
    plt.style.use('default')
    # plt.style.use('bmh')
    plt.style.use('seaborn-bright')
    font1 = {
             'weight': 'normal',
             'size': 20,
             }
    plt.xlabel("-Dst (nT)", font1)
    plt.ylabel("Complementary Cumulative (#/s.c.)", font1)
    plt.yticks(fontsize=10, color='#000000')
    plt.ylim(y0,y1)
    plt.xlim(x0,x1)
    plt.yscale("log")
    plt.xticks(fontsize=10, color='#000000')
    
    #Quebec storm
    
    Dst_quebec = 565. # nT 
    cTao_quebec=1-np.exp(-np.exp(-(Dst_quebec-mu)/sigma))
    T_quebec=1/cTao_quebec*solar_cycle

    plt.plot([Dst_quebec,Dst_quebec],[cTao_quebec,y0],linewidth=5,color='blue',alpha=0.5)
    plt.plot([x0,Dst_quebec],[cTao_quebec,cTao_quebec],linewidth=5,color='blue',alpha=0.5)
    plt.text(Dst_quebec-50,0.00001,'Quebec Storm',rotation=90,fontsize=15,horizontalalignment='center')

    
    # Carrington Storm 
        
    Dst_Carr0 = 850. # nT 
    Dst_Carr1 = 1050. # nT 
    cTao_quebec0=1-np.exp(-np.exp(-(Dst_Carr0-mu)/sigma))
    cTao_quebec1=1-np.exp(-np.exp(-(Dst_Carr1-mu)/sigma))
    T_quebec0=1/cTao_quebec0*solar_cycle
    T_quebec1=1/cTao_quebec1*solar_cycle
    
    #  horizontal part plus triangle 
    x_curve= [x0,Dst_Carr0,Dst_Carr1]
    y1_curve=[cTao_quebec1,cTao_quebec1,cTao_quebec1]
    y2_curve=[cTao_quebec0,cTao_quebec0,cTao_quebec1]
    plt.fill_between(x_curve, y1_curve,y2=y2_curve, facecolor='#87CEFA', alpha=0.5)
    
    #  vertical part 
    x_curve= [Dst_Carr0,Dst_Carr1]
    y1_curve=[y0,y0]
    y2_curve=[cTao_quebec1,cTao_quebec1]
    plt.fill_between(x_curve, y1_curve,y2=y2_curve, facecolor='#87CEFA', alpha=0.5)
    
    plt.text((Dst_Carr0+Dst_Carr1)*0.5,0.000001,'Carrington Storm',rotation=90,fontsize=15,horizontalalignment='center')
    
    plt.savefig('figure/disaster-scale.pdf')
    
    
    


#%%
# GEV = True  # T
if GEV: 
    mu= 401.295 # nT
    sigma = 128.647 # nT
    xi=-0.018
    zero_xi = False
    T_int=np.array([11.01, 22, 33, 55, 110, 1000, 10000,100000,1000000])/solar_cycle #  duration in solar cycle
    a = np.append(np.arange(0.01, 100.01, 0.1), np.arange(100.01, 100000000.01, 10))
    T_x = a/solar_cycle
    event_scale= 1./(T_int)
    event_scale_x = 1. / T_x
    y = np.log10(event_scale_x)
    quantile_x_T = mu+sigma/xi*((-np.log(1-event_scale))**(-xi) -1)
    x = mu+sigma/xi*((-np.log(1-event_scale_x))**(-xi) -1)
    #作图
    plt.plot(x, y, 'r', markersize=100)
    #1-in-11
    plt.scatter(150.8, 0.0003946, s=5, color='b')
    plt.plot([150.8, 150.8], [8, -1], '--', color='grey', lw=2)
    plt.annotate(r'1-in-11', xy=(150.8,0.0003946), xytext=(0,33), textcoords='offset points', fontsize=10,
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    #1-in-22
    plt.scatter(447.8, 0.30103, s=5, color='b')
    plt.plot([447.8, 447.8], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-22', xy=(447.8, 0.30103), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    #1-in-33
    plt.scatter(516.7,  0.477121, s=5, color='b')
    plt.plot([516.7, 516.7], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-33', xy=(516.7, 0.477121), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    #1-in-55
    plt.scatter(593.4, 0.699, s=5, color='b')
    plt.plot([593.4, 593.4], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-55', xy=(593.4, 0.699), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-110
    plt.scatter(689.7, 1, s=5, color='b')
    plt.plot([689.7, 689.7], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-110', xy=(689.7, 1), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-1000
    plt.scatter(979.1, 1.9586, s=5, color='b')
    plt.plot([979.1, 979.1], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-1000', xy=(979.1, 1.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-10000
    plt.scatter(1275.5, 2.9586, s=5, color='b')
    plt.plot([1275.5, 1275.5], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-10000', xy=(1275.5, 2.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-100000
    plt.scatter(1571.2, 3.9586, s=5, color='b')
    plt.plot([1571.2, 1571.2], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-100000', xy=(1571.2, 3.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-1000000
    plt.scatter(1866.8, 4.9586, s=5, color='b')
    plt.plot([1866.8, 1866.8], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-1000000', xy=(1866.8, 4.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # Q
    plt.scatter(565, 0.61182, s=5, color='b')
    plt.plot([565, 565], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-1000000', xy=(1866.8, 4.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-1000000
    plt.scatter(850, 4.9586, s=5, color='b')
    plt.plot([850, 850], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-1000000', xy=(850, 4.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    # 1-in-1000000
    plt.scatter(1050, 4.9586, s=5, color='b')
    plt.plot([1050, 1050], [8, -1], '--', color='grey', lw=2)
    # plt.annotate(r'1-in-1000000', xy=(1866.8, 4.9586), xytext=(0, 33), textcoords='offset points', fontsize=10,
    #              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))
    plt.show()
