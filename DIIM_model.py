#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:30:25 2023

@author: yuandingding
"""
import numpy as np 


# T_dur in hours

def diim(q0_vec,qT_vec,T_dur,x_vec,c_vec,Z_mat):

    # Calculate the Leontief coefficient matrix for the demand-side I-O model
    # Technical coefficient matrix
    A_mat = np.zeros_like(Z_mat)  # create a zeros matrix with the same size as Z_mat
    Ni = len(x_vec) # number of sectors
    # Apply Eq. 41 Lian & Haimes 2006
    # x_ij/x_j for every j
    # divide the jth colomn with x_j
    for i in range(Ni):
        A_mat[:, i] = Z_mat[:, i] / x_vec[i]


    As = np.zeros_like(A_mat)  # As
    x_mat = np.diag(x_vec)  # diag (x_vec)
    #  Note the difference between element-by-element multiplication and matrix multiplication
    As = np.linalg.inv(x_mat) @ A_mat @ x_mat
    #A_mat
    
    # To visulization == Heatmap

    # to get perturbation vector
    # to get K matrix
 
#    soi = np.zeros(Ni)
#    soe = 0
    # name_indtr=[]

  

    K_vec = np.zeros(Ni)  # K in vector form
    ## to treat cases with q_T > q_0

    #for i in range(Ni):
    #    K_vec[i] = np.log(q0_vec[i] / qT_vec[i]) / (T_dur * (1 - As[i, i])) 
    # Unit: [T^-1]
    K_vec = np.log(q0_vec / qT_vec) / (T_dur * (1 - As.diagonal()))  
    K_mat = np.diag(K_vec)  # K in diagnonal matrix form

    # sorted(u_vec,reverse=True)
    # q0_vec[25]= 0.01

    ## q_T is a vector
    # q_T=np.ones(Ni)*qe_T
    # Calculate the final demand reduce
    # Eq. 25, Lian & Haimes, 2006, system engineering, 9, 3
    # Demand reduction at time = infinity 
    As_I = As - np.eye(Ni, dtype=float)
    cs0 = -As_I @ qT_vec
    # demand reduction in currency 
    # dc0 = x_mat @ cs0
    # sorted(dc0,reverse=True)

    #dt = 1  # time step, 1 time unit
    #Nt = int(T_dur / dt) + 1
    Nt = 1001 # number of point for integration
    dt = T_dur/float(Nt-1) # [T]
    #print(Nt,dt)
    #  if NT < 100 give an warning
    time = np.linspace(0, T_dur, num=Nt, endpoint=True)
    # time.shape
#    qk_vec = q0_vec  # Inoperability at time k
#    qk1_vec = q0_vec  # Inoperability at time k+1
    qt_vec = np.zeros((Ni, Nt), dtype=float)  # Inoperability vector to contain all qk vector
    qt_vec[:, 0] = q0_vec
    #  qt_vec[:, 1] = q0_vec
    #  q0_vec  # set initial value for time=0
    # cs_t = np.zeros( (Ni, Nt),dtype=float )
    # Permanent demand reduction
    cs_t = np.tile(cs0, (Nt, 1)).transpose()  

    # cs_t.shape
    # qt_vec.shape

    year=24*360.
    for k in range(Nt-1):
        qt_vec[:, k + 1] = qt_vec[:, k] + dt * K_mat @ ((As_I @ qt_vec[:, k]) + cs_t[:, k])
    #  Integration includes a dimension of time, it should be normalized with a year, the fiscal year.   
    Q_loss = np.sum(qt_vec,axis=1)*dt/year*x_vec

    return qt_vec,time, Q_loss


