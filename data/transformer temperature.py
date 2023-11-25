import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Idc_to_dT(Idc):
  """ convert GIC into a asymptoptic temperature rise
      Figure 2 & 3 for  hot-spot of winding and flitch plate. Marti, IEEE pow. del. 2013, 28
  """
  scale_factor = 100./50. # this factor varies with transformer model
  return Idc*scale_factor

def Temperature_rise(alpha,n):
  #  Reproduce Figure 1 Marti, IEEE pow. del. 2013, 28
  # %%
  alpha0 = alpha * sixty  # 2.5 minutes
  t_max = 6 * alpha0  # 5*alpha times of typical time scale for calculations
  #  ensure that time inverval is consistent with GIC calculation
  Nt_pulse = int(np.ceil(t_max / dt) + 1)
  time_for_pulse = np.linspace(0, t_max, num=Nt_pulse, endpoint=True)
  ht_model = 1.0 / alpha0 * np.exp(-time_for_pulse / alpha0)

  GIC_abs = abs(data2.iloc[:, n + 1].values)

  GIC_padding = np.zeros_like(ht_model)
  Np = Nt_pulse
  dtemp_trans = np.zeros_like(GIC_abs)
  GIC_test = np.zeros_like(GIC_abs)

  GIC_abs_with_padding = np.concatenate((GIC_padding, GIC_abs, GIC_padding))

  for k in range(Nt):  # range(NT):
    ht_pulse = ht_model * Idc_to_dT(GIC_abs_with_padding[Np + k:Np + k + Nt_pulse])
    ht_pulse_rev = np.flip(ht_pulse)
    dtemp_trans[k] = sum(ht_pulse_rev * GIC_abs_with_padding[k:k + Nt_pulse])

  maxt.append(max(dtemp_trans))


disater_csv_name = ['1989-11.csv', '1989-22.csv', '1989-33.csv', '1989-55.csv',
                 '1989-110.csv', '1989-1000.csv', '1989-10000.csv',
                 '1989-100000.csv', '1989-1000000.csv']

disaster_filename = ['Temperature_1989-11.csv', 'Temperature_1989-22.csv', 'Temperature_1989-33.csv', 'Temperature_1989-55.csv',
                 'Temperature_1989-110.csv', 'Temperature_1989-1000.csv', 'Temperature_1989-10000.csv',
                 'Temperature_1989-100000.csv', 'Temperature_1989-1000000.csv']


sixty = 60.0
thousand = 1000.
mega = 1000000.
node_numbers = 387
disater_level_number = 9

data1 = pd.read_csv(r'max_uk_gic8.28.csv')  #for循环
data3 = pd.read_csv(r'12.16 voltage(1).csv')
# print(data3.iloc[7]['voltage'])

for i in range(disater_level_number):
  data2 = pd.read_csv(disater_csv_name[i])
  Nt = data2.shape[0] #number of time steps
  Nn = data2.shape[1]-1 # number of nodes, -1 will remove the time frame
  data2['datetime'] = pd.to_datetime(data2['datetime'])
  data2.set_index('datetime')

  GIC_max = data2.max(axis=0,numeric_only=True)
  GIC_min = data2.min(axis=0,numeric_only=True)

  node_in_use = '1512'

  node_number = data2.columns[1:] # skip time frame
  timestamp = data2['datetime']
  time_in_sec=(timestamp-timestamp[0]).dt.total_seconds() # convert deltatime into seconds
  time_in_sec=time_in_sec.values # convert into seconds as array
  #GIC_abs=abs(data2[node_in_use].values)
  # GIC_abs=abs(data2[1:,0:1].values) # take only amplitudes
  dt = time_in_sec[1]-time_in_sec[0] # time interval, 60 second, 1 minute


  maxt = []
  for n in range(node_numbers):  #循环492个点
    if data3.iloc[n-2]['voltage'] == 400:#转成字符串判断
      alpha = 3.2
      Temperature_rise(alpha, n)
    else:
      alpha = 2.5
      Temperature_rise(alpha, n)

  data1 = pd.DataFrame(maxt)
  data1.to_csv(disaster_filename[i])