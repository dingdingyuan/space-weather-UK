# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 09:30:25 2023

@author: wangxian
"""
import numpy as np
import pandas as pd
from DIIM_model import diim

def extract_Z(No_sectors):
    # %%
    # 导入数据

    df = pd.read_excel('data/nasu1719pr.xlsx', sheet_name="IOT", header=4)
    df = df.drop(index=0)
    No_sectors = No_sectors
    number_product = 105
    # print(f'共导入{number_product}行数据')
    z = np.array(df.iloc[:number_product, 2:2 + No_sectors])
    x = np.array(df["Total"].tolist()[:No_sectors])
    c = np.array(df["Total Use at basic prices"].tolist()[:No_sectors])
    list_sectors = df["Product"].tolist()[:No_sectors]

    # 按下标删去list
    def list_del(list_given, index_to_delete):
        for counter, index in enumerate(index_to_delete):
            index = index - counter
            list_given.pop(index)
        return list_given

    # 查全零行列
    def index_all_zero(z):
        list_allzero = []
        for i in range(z.shape[0]):
            buckle = 0
            for j in range(z.shape[1]):
                if z[i][j] == 0:
                    buckle += 1
            if buckle == z.shape[1]:
                list_allzero.append(i)
        return list_allzero

    # 删除干扰行
    z1 = np.delete(z, index_all_zero(z), axis=0)
    z1 = np.delete(z1, index_all_zero(z), axis=1)
    c = np.delete(c, index_all_zero(z), axis=0)
    x = np.delete(x, index_all_zero(z), axis=0)

    z1 = np.delete(z1, 1, axis=0)
    z1 = np.delete(z1, 1, axis=1)
    c = np.delete(c, 1, axis=0)
    x = np.delete(x, 1, axis=0)

    list_sectors = list_del(list_sectors, [1, 77, 104])
    # print("删去下标如下的几行列\n", [1, 77, 104])
    Z_mat = z1
    x_vec = x
    c_vec = c
    Ni = number_product - 3

    # print("Z矩阵形状为：", Z_mat.shape)
    print(x_vec.shape)
    print(np.diag(x_vec))
    print("Data read complete\n\n")
    return Z_mat,x_vec,c_vec,Ni,list_sectors

def select_loss_top5(qe_scales,Ni,T_scales,q0_vec,qT_vec,x_vec,c_vec,Z_mat,list_sectors):
    # 损失最大前5
    #Select the 5 sectors with the largest calculated losses
    # print("开始计算损失最大的top5行业\n说明：认为各时期在top5次数最多的前5个行业是所求")

    def reverse_order(list_lost):
        x = list_lost
        b = sorted(enumerate(x), key=lambda x: x[1], reverse=True)  # x[1]是因为在enumerate(a)中，a数值在第1位
        c = [x[0] for x in b]  # 获取排序好后b坐标,下标在第0位
        return c

    list_Inoperability = qe_scales

    # list_Inoperability[0] =  0.0401507663845142
    data_plot = pd.DataFrame({
        'time': [],
        'Inoperability': [],
        "scenario": [],
        "product": [],
    })
    product_lost5 = []
    scoreboard = np.zeros(Ni)
    for i in range(len(list_Inoperability)):
        T_dur = T_scales[i]
        qt_vec, time, Q_loss = diim(q0_vec, qT_vec, T_dur, x_vec, c_vec, Z_mat)
        # 排序
        # 前5损失行业下标
        for j in range(5):
            scoreboard[reverse_order(Q_loss)[j]] += 1

    # print(reverse_order(scoreboard)[:5])
    # [3, 5, 74, 47, 50]

    product_lost5 = list(set(reverse_order(scoreboard)[:5]))
    print("The subscript of the top5 industry with the largest loss is：", product_lost5, "\n The name is as follows：")
    for i in range(len(product_lost5)):
        print(list_sectors[product_lost5[i]])

    print("\n\n")
    return product_lost5