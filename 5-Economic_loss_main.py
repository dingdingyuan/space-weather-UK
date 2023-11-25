#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from DIIM_model import diim
from Extract_data import extract_Z,select_loss_top5
from Economic_Loss_Mapping import *
#%%

#导入数据

Z_mat,x_vec,c_vec,Ni,list_sectors = extract_Z(105)

#%%
#  To estimate paramters for DIIM model 
# 
sixty = 60. 
twenty_four=24. 
days_of_year =360.


# negative estimate
# inop_neg = pd.read_csv("Inoperability_substation_series_negative.csv")
inop_neg = pd.read_csv("data/Inoperability_v2.csv")
disaster_scales = inop_neg.scenario.values.tolist()
qe_scales_neg = inop_neg.Inoperability.values.tolist()
# positive estimate
# inop_pos = pd.read_csv("Inoperability_substation_series_positive.csv")
inop_pos = pd.read_csv("data/Inoperability_v1.csv")
disaster_scales = inop_pos.scenario.values.tolist()
qe_scales_pos = inop_pos.Inoperability.values.tolist()
# mean estimate
qe_scales = [(x + y) / 2 for x, y in zip(qe_scales_neg, qe_scales_pos)]




#parameter setting

Nd_scales = len(disaster_scales)
waiting_time = np.array(['11', '22','33', # 0, 1, 2
                        '55','110', '1000', # 3, 4, 5, 
                        '10000', '100000', '1000000']) # 6, 7, 8
# in seconds
#T = 7200.  # 1 -33 ：48h - 1 week 55-1000：1week - 1m 1000abvoe：2m-2y       
#  Recovering period 12 h, 720 min #变压器维修时间
#  in      hours     11   22   33     55      110     10000   10,000      100,000      1,000,000
T_scales = np.array([24, 24*7,  24*30,  24*30*2,  24*30*6,  24*30*12,24*30*12*2, 24*30*12*5 ,24*30*12*10])
kscale =  0
T_dur = T_scales[kscale]
ie = 49  # index for electricity industry
q0_elec = qe_scales[kscale] # shock to the electricity industry
## build an dictionary to index the industry number
# u_vec = np.zeros_like(x_vec)
#for i in range(Ni):
u_vec = Z_mat[ie,:] / x_vec  # share of electricity in the output of industry 𝑖 d
u_max = max(u_vec)
q0_vec = q0_elec * u_vec / u_max  # perturbation vT_scales[kscale]ector
## This value would render increase in some industry
qe_T = 0.0001  # top .001-.01   #1/10000 - 1/1000  #  inoperability level at time T
qT_vec = np.ones(Ni) * qe_T
isectors_to_assess = [3, 49, 74, 47, 50]
qT_vec[isectors_to_assess] = 0.001  # Set 


# Select the 5 sectors with the largest calculated losses
product_lost5 = select_loss_top5(qe_scales,Ni,T_scales,q0_vec,qT_vec,x_vec,c_vec,Z_mat,list_sectors)

# drawing
dynamic_graph(list_sectors,product_lost5,T_scales,qe_scales,qT_vec,x_vec, c_vec, Z_mat)

Histogram_Loss_graph(list_sectors,product_lost5,T_scales,qe_scales,qT_vec,x_vec, c_vec, Z_mat,qe_scales_pos,qe_scales_neg)

# Histogram_Inop_graph(list_sectors,product_lost5,T_scales,qe_scales,qT_vec,x_vec, c_vec, Z_mat,qe_scales_pos,qe_scales_neg)

three_in_one_graph(list_sectors,product_lost5,T_scales,qe_scales,qT_vec,x_vec, c_vec, Z_mat,qe_scales_pos,qe_scales_neg)


#picture_integration
# picture_integration()
picture_integration_Simplified()
