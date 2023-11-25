import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""

IEEE C57.91 1995 suggestion on maximum temperature limts
Insulated conductor hottested-spot temperature

120 C for normal life expectation loading
130 C for planned loading beyond nameplate rating
140 C for Long-time emergency loading
180 C for short-time emergency loading



#%% Estimate the probability of failure with temperature distribution

2022-11-18 (DY)

Assume the probability of failure has an Weibull distiribution
Weibull distribution is normally applied to electric devices,
it has two parameters to estimate and therehence the model become more complicated.
We assume that if the temperature of an transformer reached the limit suggested by IEEE,
then it has probability of p=0.002699796063	 to survive, which is equivalane to 3*sigma in normal distribution
1-exp(-lambra*dT) = 1-p
-log(p) = lambda*dT
# uncertainties could be estimated by considering full-load and non-load conditions

Assume ambient temperataure T0= 65
(1) Optimistic estimates


When T = 130, the probability of failure is 1-p = 0.997300203937 (or 3*sigma equivalent)

# Eq. 11, Dehghanian & Overbye, 2021 IEEE Texas Power and Energy Conference (TPEC), 2021, pp. 1-6,

T_final = T_hs+ T_oil+ T_ambient

T_ambient = 30 degree
T_oil = 45 degree

(2) Pessimistic estimate

When T = 120, the probability of failure is 1-p = 0.997300203937 (or 3*sigma equivalent)
((T_max-T0)/T_lambda)^K = - log(p)
(T_max-T0)/T_lambda = [-log(p)]^{1/K}

"""

KT = 1.5
T_lambda = 100

T_ambient = 30  #  ambient temperature
T_oil = 45 # top oil temperature
p0 = 0.002699796063

# At T=T0, the probability of failure is 0
# At T = T_max, the probability of failure  is 1-p0
T0 = T_ambient + T_oil

T_max0 = 120
T_lambda0 = (T_max0-T0)/(-np.log(p0))**(1/KT)
# print(T_lambda0)

N_T = 60
T_grid0 = np.linspace(T0, T_max0,N_T)
P_cum0 = 1-np.exp(-((T_grid0-T0)/T_lambda0)**KT)

T_max1 = 130
T_lambda1 = (T_max1-T0)/(-np.log(p0))**(1/KT)
# print(T_lambda1)

N_T = 60
T_grid1 = np.linspace(T0, T_max1,N_T)
P_cum1 = 1-np.exp(-((T_grid1-T0)/T_lambda1)**KT)

import math

node_numbers = 387
disater_level_number = 9
disaster_filename = ['Temperature_1989-11.csv', 'Temperature_1989-22.csv', 'Temperature_1989-33.csv', 'Temperature_1989-55.csv',
                 'Temperature_1989-110.csv', 'Temperature_1989-1000.csv', 'Temperature_1989-10000.csv',
                 'Temperature_1989-100000.csv', 'Temperature_1989-1000000.csv']

disaster_name_1 = ['1989-11-1.csv', '1989-22-1.csv', '1989-33-1.csv', '1989-55-1.csv',
                 '1989-110-1.csv', '1989-1000-1.csv', '1989-10000-1.csv',
                 '1989-100000-1.csv', '1989-1000000-1.csv']

disaster_name_2 = ['1989-11-2.csv', '1989-22-2.csv', '1989-33-2.csv', '1989-55-2.csv',
                 '1989-110-2.csv', '1989-1000-2.csv', '1989-10000-2.csv',
                 '1989-100000-2.csv', '1989-1000000-2.csv']

for n in range(disater_level_number):
    data1 = pd.read_csv(disaster_filename[n])
    maxt = data1.iloc[:,1]
    p_cum1 = []
    p_cum2 = []
    maxt = np.array(maxt)
    for i in range(node_numbers):
      maxt[i] = maxt[i] + T_ambient + T_oil
      p_cum1.append(1 - math.exp(-((maxt[i] - T0) / T_lambda1) ** KT) )
      p_cum2.append(1 - math.exp(-((maxt[i]-T0)/T_lambda0)**KT) )

    data1 = pd.DataFrame(p_cum1)
    data2 = pd.DataFrame(p_cum2)
    data1.to_csv(disaster_name_1[n])
    data2.to_csv(disaster_name_2[n])

# print(p_cum1)
