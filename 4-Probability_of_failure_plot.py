"""
UK Space Weather Analysis (python)
————Figures

author：王贤
time：2022.11.21



This program draws the sub-graphs of figure.3
Probability of failure currently uses a conservative estimate (before update)


"""
##############################
# 并联 negative
##############################


import pandas as pd

# population = pd.read_csv("population.csv")
#
# list_population = population['population'].tolist()
#
# sum_population = sum(list_population)


# 画图用数据

dic = {
    "scenario": [],  # 列表
    "failure": [],  # 数组
    "Easting": [],
    "Northing": [],
}
data_plot = pd.DataFrame(dic)
n_row = 0
list_scenario=["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"]
# print(data1)
list_failure = ["0%-12.5%",'12.5%-25%','25%-37.5%','37.5%-50%','50%-62.5%','62.5%-75%','75%-87.5%','87.5%-100%']
#分级



#变电站人口数据
population = pd.read_csv("data/df_sub_popu_number.csv")
list_population = population['population'].tolist()
sum_population = sum(list_population)


#数据总人口
# print(sum_population)

#变压器失败数据
file_list2 = ['1989-11-2.csv','1989-22-2.csv','1989-33-2.csv','1989-55-2.csv','1989-110-2.csv','1989-1000-2.csv','1989-10000-2.csv','1989-100000-2.csv','1989-1000000-2.csv']

file_list1 = ['1989-11-1.csv','1989-22-1.csv','1989-33-1.csv','1989-55-1.csv','1989-110-1.csv','1989-1000-1.csv','1989-10000-1.csv','1989-100000-1.csv','1989-1000000-1.csv']

# for -1

# df=pd.read_csv(f'failure\{file_list[1]}')
df=pd.read_csv(rf'data/{file_list2[1]}')

failure_rate = df.iloc[:,1].tolist()

# print(failure_rate)

list_failure_population = []
for i in range(len(list_population)):
    list_failure_population.append( list_population[i] * failure_rate[i])


# print(sum(list_failure_population)/sum_population)

list_inop = []
for k in range(9):
    # df = pd.read_csv(rf'failure\update\{file_list[k]}')
    df = pd.read_csv(rf'data/{file_list1[k]}')
    # df = pd.read_csv(rf'failure\update2\{file_list2[k]}')
    failure_rate = df.iloc[:, 1].tolist()

    # print(failure_rate)

    # for failure_rate_substation
    failure_rate_substation = []
    for i in range(len(list_population)):
        failure_rate_persubstation = 1
        #per_transformer 1 - failure_rate


        # substation直接看作node
        s = failure_rate[i]
        failure_rate_substation.append(s)

        # 填充画图数据

        failure_level = int((s) // 0.125)
        if failure_level >= 7:
            failure_level = 7
        data_plot.loc[n_row] = [list_scenario[k], s, population['Easting'][i], population['Northing'][i]]
        n_row = n_row + 1



    list_failure_population = []
    for i in range(len(list_population)):
        list_failure_population.append(list_population[i] * failure_rate_substation[i])

    print(sum(list_failure_population) / sum_population)
    list_inop.append(sum(list_failure_population) / sum_population)
dic = {
    "scenario": [],  # 列表
    "Inoperability": [],  # 数组

}
data = pd.DataFrame(dic)
list_scenario=["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"]
for i in range(9):
    data.loc[i] = [list_scenario[i] , list_inop[i] ]

# print(data["scenario"].tolist())

# 保存
data.to_csv("data/Inoperability_v1.csv")
data_plot.to_csv("data/failure_substation_v1.csv")



dic = {
    "scenario": [],  # 列表
    "failure": [],  # 数组
    "Easting": [],
    "Northing": [],
}
data_plot = pd.DataFrame(dic)




# for -2

# df=pd.read_csv(f'failure\{file_list[1]}')
df=pd.read_csv(rf'data/{file_list2[1]}')

failure_rate = df.iloc[:,1].tolist()

# print(failure_rate)

list_failure_population = []
for i in range(len(list_population)):
    list_failure_population.append( list_population[i] * failure_rate[i])


# print(sum(list_failure_population)/sum_population)

list_inop = []
for k in range(9):
    # df = pd.read_csv(rf'failure\update\{file_list[k]}')
    df = pd.read_csv(rf'data/{file_list2[k]}')
    # df = pd.read_csv(rf'failure\update2\{file_list2[k]}')
    failure_rate = df.iloc[:, 1].tolist()

    # print(failure_rate)

    # for failure_rate_substation
    failure_rate_substation = []
    for i in range(len(list_population)):
        failure_rate_persubstation = 1
        #per_transformer 1 - failure_rate


        # substation直接看作node
        s = failure_rate[i]
        failure_rate_substation.append(s)

        # 填充画图数据

        failure_level = int((s) // 0.125)
        if failure_level >= 7:
            failure_level = 7
        data_plot.loc[n_row] = [list_scenario[k], s, population['Easting'][i], population['Northing'][i]]
        n_row = n_row + 1



    list_failure_population = []
    for i in range(len(list_population)):
        list_failure_population.append(list_population[i] * failure_rate_substation[i])

    print(sum(list_failure_population) / sum_population)
    list_inop.append(sum(list_failure_population) / sum_population)
dic = {
    "scenario": [],  # 列表
    "Inoperability": [],  # 数组

}
data = pd.DataFrame(dic)
list_scenario=["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"]
for i in range(9):
    data.loc[i] = [list_scenario[i] , list_inop[i] ]

# print(data["scenario"].tolist())

# 保存
data.to_csv("data/Inoperability_v2.csv")
data_plot.to_csv("data/failure_substation_v2.csv")


# ##############################
# # 并联 positive
# ##############################
# list_inop = []
# dic = {
#     "scenario": [],  # 列表
#     "failure": [],  # 数组
#     "Easting": [],
#     "Northing": [],
# }
# data_plot = pd.DataFrame(dic)
#
# file_list = ['1989-11-1.csv','1989-22-1.csv','1989-33-1.csv','1989-55-1.csv','1989-110-1.csv','1989-1000-1.csv','1989-10000-1.csv','1989-100000-1.csv','1989-1000000-1.csv']
#
# for k in range(9):
#     # df = pd.read_csv(rf'failure\update\{file_list[k]}')
#     df = pd.read_csv(rf'5-Probability_of_failure-data/failure\update2\{file_list[k]}')
#     # df = pd.read_csv(rf'failure\update2\{file_list2[k]}')
#     failure_rate = df.iloc[:, 1].tolist()
#
#     # print(failure_rate)
#
#     # for failure_rate_substation
#     failure_rate_substation = []
#     for i in range(len(list_population)):
#         failure_rate_persubstation = 1
#         #per_transformer 1 - failure_rate
#
#
#         # #串联算法
#         # list_sum = []
#         # for j in range(len(match[i])):
#         #     list_sum.append(1 - failure_rate[match[i][j]])
#         # #accumulation
#         # s = 1
#         # for x in list_sum:
#         #     s *= x
#         # s = 1 - s
#         # failure_rate_substation.append(s)
#         # # 串联算法结束
#
#         # # 并联算法
#         # list_sum = []
#         # for j in range(len(match[i])):
#         #     list_sum.append(failure_rate[match[i][j]])
#         # # accumulation
#         # s = 1
#         # for x in list_sum:
#         #     s *= x
#         # failure_rate_substation.append(s)
#         # # 并联算法结束
#
#         # max算法
#         list_sum = []
#         for j in range(len(match[i])):
#             list_sum.append(failure_rate[match[i][j]])
#         # accumulation
#         s = max(list_sum)
#         failure_rate_substation.append(s)
#         # max算法结束
#
#
#         # 填充画图数据
#
#         failure_level = int((s) // 0.125)
#         if failure_level >= 7:
#             failure_level = 7
#         data_plot.loc[n_row] = [list_scenario[k], s, population['Easting'][i], population['Northing'][i]]
#         n_row = n_row + 1
#
#
#     list_failure_population = []
#     for i in range(len(list_population)):
#         list_failure_population.append(list_population[i] * failure_rate_substation[i])
#
#     print(sum(list_failure_population) / sum_population)
#     list_inop.append(sum(list_failure_population) / sum_population)
# dic = {
#     "scenario": [],  # 列表
#     "Inoperability": [],  # 数组
#
# }
# data = pd.DataFrame(dic)
# list_scenario=["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"]
# for i in range(9):
#     data.loc[i] = [list_scenario[i] , list_inop[i] ]
#
# print(data["scenario"].tolist())
#
# # 保存
# data.to_csv("Inoperability_substation_series_positive.csv")
#
# data_plot.to_csv("5-Probability_of_failure-data/failure_substation_series_positive_v2.csv")
#

######################
## PLOT mean
######################

q_list = ["Q1","Q2","Q3","Q4","Q5","Q6","Q7","Q8"]

import pandas as pd
import numpy as np

# 计算平均数据
data_pos = pd.read_csv("data/failure_substation_v1.csv")
data_neg = pd.read_csv("data/failure_substation_v2.csv")

data_mean = (data_pos['failure'] + data_neg['failure']) / 2

data_pos['failure'] = data_mean
data = data_pos
data_pos = pd.read_csv("data/failure_substation_v1.csv")
def get_level(data):
    list_failurelevel_mean = []
    list_failure = ["0%-12.5%", '12.5%-25%', '25%-37.5%', '37.5%-50%', '50%-62.5%', '62.5%-75%', '75%-87.5%',
                    '87.5%-100%']
    for i in range(len(data)):
        failure_level = int((data["failure"][i]) // 0.125)
        if failure_level >= 7:
            failure_level = 7

        list_failurelevel_mean.append(q_list[failure_level])

    data['failure'] = list_failurelevel_mean
    return data

# 重新分级
list_failurelevel_mean = []
list_failure = ["0%-12.5%",'12.5%-25%','25%-37.5%','37.5%-50%','50%-62.5%','62.5%-75%','75%-87.5%','87.5%-100%']
for i in range(len(data)):
    failure_level = int((data["failure"][i]) // 0.125)
    if failure_level >= 7:
        failure_level = 7

    list_failurelevel_mean.append(list_failure[failure_level])

data['failure'] = list_failurelevel_mean
print(data)
import geopandas as gpd
import pandas as pd
from plotnine import *
from plotnine import ggplot, geom_map, aes, scale_fill_cmap, theme, labs
from plotnine import geom_point
import plotnine as p9

######################
import pandas as pd

tran = data



#地图

tran['scenario1'] = tran['scenario'].astype('category')
tran['scenario1'] = tran['scenario1'].cat.reorder_categories(["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"],ordered=True)

tran['failure1'] = tran['failure'].astype('category')
tran['failure1'] = tran['failure1'].cat.reorder_categories(list_failure,ordered=True)



shp = gpd.read_file('data/all.shp')
p = (
ggplot()
+geom_map(data=shp,color = "grey",fill="#F5F5F5", size = 0.3 ,alpha=0.8)
+geom_point(data=tran,mapping=aes(x='Easting', y='Northing', size='pd.Categorical(failure1)',
                                              colour='pd.Categorical(failure1)'), alpha=0.3)
+ labs(title="",x = '',y = '')
+ coord_equal(expand=False)
+ facet_wrap("scenario1",
             nrow=3 ,
        # change the number of columns
             )
# +guides(fill = guide_legend(reverse = False))
+ scale_colour_manual(name = "  ",values=["#999999","#666666","#80FF00","#00FF80","#FFD700","#FF8000","brown","#FF0000"],labels = q_list)
+ scale_size_manual(name = "  ",values=[1, 2, 3, 4, 5, 6, 7 ],labels =q_list, na_value = 8)
#+ scale_color_brewer(type='qual', palette=2)
# + lims(x=(1000, 70000))
+ annotate('text', x=0, y=0,label='50+', size=100, color='black', va='top')
+ theme_dark()
+ theme(
    dpi=300,
    axis_text_x = element_blank(),
    axis_text_y = element_blank(),
    #aspect_ratio=1   # height:width
    axis_text = p9.themes.element_text(size = 5, color = "#999999"),
    legend_text=element_text(hjust = 1,size = 10,weight = "heavy"),
    axis_title = element_text(hjust = 1,vjust = 1),
    title = element_text(hjust = 0.5,vjust = 0),
    legend_title = element_text(hjust = 0,vjust = 0),
    legend_direction='vertically',
    legend_position=[0.35, 0.829],
    legend_key_size =0.01,
    legend_entry_spacing_y = 5,
    legend_background = element_rect(fill= "#F5F5F5",size = 3 ,color = "grey"  ),
    legend_box_margin = 5,
    plot_title = element_text(size = 13,weight = "heavy"),
    strip_text_x = element_text(size = 18,weight = "heavy"),
    # axis_text = element_text(size = 13,weight = "heavy"),
    # legend_text = element_text(size = 13,weight = "heavy"),

)
)

fig = p.draw()
fig.set_size_inches(10, 10, forward=True)

fig.show()
p.save('figure/Probability_of_Failure_per_substation_left.png', height=14, width=14)




# 处理dataframe
# 柱形图

tran = data
# tran["current"] = tran["current"].replace('150-175', '>150', regex=True)
# tran["current"] = tran["current"].replace('> 175', '>150', regex=True)
failure_rate_list = ["0%-12.5%",'12.5%-25%','25%-37.5%','37.5%-50%','50%-62.5%','62.5%-75%','75%-87.5%','87.5%-100%']
for i in range(len(q_list)):
    tran["failure"] = tran["failure"].replace(failure_rate_list[i], q_list[i], regex=True)






# current_list = ['0-25', '25-50', '50-75', '75-100', '100-125',  '125-150', '150-175','> 175']
current_list = ['0-25', '25-50', '50-75', '75-100', '100-125',  '125-150', '>150']


tran1 = tran[(tran['scenario'] == '1-in-11') |(tran['scenario'] == '1-in-22') |(tran['scenario'] == '1-in-33')]
tran2 = tran[(tran['scenario'] == '1-in-55') |(tran['scenario'] == '1-in-110') |(tran['scenario'] == '1-in-1,000')]
tran3 = tran[(tran['scenario'] == '1-in-10,000') |(tran['scenario'] == '1-in-100,000') |(tran['scenario'] == '1-in-1,000,000')]
alpha = 0.7

data_pos = get_level(data_pos)
tran1_pos = data_pos[(data_pos['scenario'] == '1-in-11') |(data_pos['scenario'] == '1-in-22') |(data_pos['scenario'] == '1-in-33')]
tran2_pos = data_pos[(data_pos['scenario'] == '1-in-55') |(data_pos['scenario'] == '1-in-110') |(data_pos['scenario'] == '1-in-1,000')]
tran3_pos = data_pos[(data_pos['scenario'] == '1-in-10,000') |(data_pos['scenario'] == '1-in-100,000') |(data_pos['scenario'] == '1-in-1,000,000')]

data_neg = get_level(data_neg)
tran1_neg = data_neg[(data_neg['scenario'] == '1-in-11') |(data_neg['scenario'] == '1-in-22') |(data_neg['scenario'] == '1-in-33')]
tran2_neg = data_neg[(data_neg['scenario'] == '1-in-55') |(data_neg['scenario'] == '1-in-110') |(data_neg['scenario'] == '1-in-1,000')]
tran3_neg = data_neg[(data_neg['scenario'] == '1-in-10,000') |(data_neg['scenario'] == '1-in-100,000') |(data_neg['scenario'] == '1-in-1,000,000')]

def count_cul(tran2,level_3):
    dic = {
        "scenario": [],  # 列表
        "failure": [],
        "counts": [],  # 数组
        "error": [],
    }
    tran2_counted = pd.DataFrame(dic)
    list_scenario = ["1-in-11", "1-in-22", "1-in-33", "1-in-55", "1-in-110", "1-in-1,000", "1-in-10,000",
                     "1-in-100,000", "1-in-1,000,000"]
    q_list = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8"]
    n_row = 0
    for i in range(level_3, level_3+3):
        counts = tran2[tran2['scenario'] == list_scenario[i]]['failure'].value_counts()
        for j in list(counts.index):


            tran2_counted.loc[n_row] = [list_scenario[i], j, counts[j], 10]
            n_row += 1
    return tran2_counted

tran1_counted = count_cul(tran1,0)
tran1_neg_counted = count_cul(tran1_neg,0)
tran1_pos_counted = count_cul(tran1_pos,0)

tran2_counted = count_cul(tran2,3)
tran2_neg_counted = count_cul(tran2_neg,3)
tran2_pos_counted = count_cul(tran2_pos,3)

tran3_counted = count_cul(tran3,6)
tran3_neg_counted = count_cul(tran3_neg,6)
tran3_pos_counted = count_cul(tran3_pos,6)



def err(tran1_counted,tran1_neg_counted,tran1_pos_counted):
    list_err = []
    for i in list(set(tran1_counted["scenario"])):
        if i == 1:
            print(list(tran1_counted[tran1_counted["scenario"] == i]["failure"]))
        for j in list(tran1_counted[tran1_counted["scenario"] == i]["failure"]):
            if tran1_neg_counted[(tran1_neg_counted["scenario"] == i) & (tran1_neg_counted["failure"] == j)]["counts"].empty:
                j_neg = 0
            else:
                j_neg = tran1_neg_counted[(tran1_neg_counted["scenario"] == i) & (tran1_neg_counted["failure"] == j)]["counts"].values[0]

            if tran1_pos_counted[(tran1_pos_counted["scenario"] == i) & (tran1_pos_counted["failure"] == j)]["counts"].empty:
                j_pos = 0
            else:
                j_pos = tran1_pos_counted[(tran1_pos_counted["scenario"] == i) & (tran1_pos_counted["failure"] == j)]["counts"].values[0]
            list_err.append(abs(j_neg - j_pos) / 2)

    tran1_counted["error"] = list_err
    return tran1_counted

tran1_counted = err(tran1_counted,tran1_neg_counted,tran1_pos_counted)
tran2_counted = err(tran2_counted,tran2_neg_counted,tran2_pos_counted)
tran3_counted = err(tran3_counted,tran3_neg_counted,tran3_pos_counted)



tran1_counted['scenario2'] = tran1_counted['scenario'].astype('category')
tran1_counted['scenario2'] = tran1_counted['scenario2'].cat.reorder_categories(["1-in-11","1-in-22","1-in-33"],ordered=True)


tran2_counted['scenario2'] = tran2_counted['scenario'].astype('category')
tran2_counted['scenario2'] = tran2_counted['scenario2'].cat.reorder_categories(["1-in-55","1-in-110","1-in-1,000"],ordered=True)


tran3_counted['scenario2'] = tran3_counted['scenario'].astype('category')
tran3_counted['scenario2'] = tran3_counted['scenario2'].cat.reorder_categories(["1-in-10,000","1-in-100,000","1-in-1,000,000"],ordered=True)

num_station = 387
break_y = [0 * num_station/5 , 1 * num_station/5, 2 * num_station/5, 3 * num_station/5, 4 * num_station/5,5 * num_station/5]

# q_list = [0,1,2,3,4,5,6,7]



qs1 = (
ggplot(data = tran1_counted)
+ geom_bar(aes(x='failure', y='counts',fill='scenario2'),size = 1.5,stat = "identity",position="dodge",color="#9c6d6d",width =0.5)
+ geom_errorbar(aes(x='failure', y='counts',ymin='counts-error', ymax='counts+error',group = 'scenario2'),color="#4c4c4c",position=position_dodge(), size=1)
+ coord_flip()
+ scale_x_discrete(limits=q_list)
+ scale_fill_manual(values = ["#e81414","#ad144a","#4a271f"]) #"#999999","#666666","#80FF00","#00FF80","#FFCC00","#FF8000","#FF0000","brown"
+ theme_dark()
+ guides(
    nrow = 3,ncol = 1
 )
+ ylim(0,num_station)
+ scale_y_continuous(limits=(0, num_station), breaks=break_y, labels=["0%", "20%", "40%", "60%", "80%","100%"])
+ labs(title=" ",x = '',y = '',fill = " ")
+ theme(
    dpi=300,
    panel_background = element_rect(fill="#fdfffd", alpha=.8),
    legend_direction='vertically',
    legend_position=[0.8, 0.9],
    legend_background = element_rect(fill= "#F5F5F5",size = 3 ,color = "grey"  ),
    axis_text = element_text(size = 13,weight = "heavy"),
    legend_text = element_text(size = 13,weight = "heavy"),
)
)

qs2 = (
ggplot(data = tran2_counted)
+ geom_bar(aes(x='failure', y='counts',fill='scenario2'),size = 1.5,stat = "identity",position="dodge",color="#9c6d6d",width =0.5)
+ geom_errorbar(aes(x='failure', y='counts',ymin='counts-error', ymax='counts+error',group = 'scenario2'),color="#4c4c4c",position=position_dodge(), size=1)
+ coord_flip()
+ scale_x_discrete(limits=q_list)
+ scale_fill_manual(values = ["#e81414","#ad144a","#4a271f"]) #"#3621b2","#0c8993","#24c578"
+ theme_dark()
+ ylim(0,num_station)
+ scale_y_continuous(limits=(0, num_station), breaks=break_y, labels=["0%", "20%", "40%", "60%", "80%","100%"])
+ labs(title=" ",x = '',y = '',fill = " ")
+ theme(
    dpi=300,
    panel_background = element_rect(fill="#fdfffd", alpha=.8),##F5F5F5
    legend_direction='vertically',
    legend_position=[0.8, 0.55],
    legend_background = element_rect(fill= "#F5F5F5",size = 3 ,color = "grey" ),
    legend_box_just = "top",
    # legend_key_width = 2,
    axis_text = element_text(size = 13,weight = "heavy"),
    legend_text = element_text(size = 13,weight = "heavy"),

)
)

# qs2.draw()

qs3 = (
ggplot(data = tran3_counted)
+ geom_bar(aes(x='failure', y='counts',fill='scenario2'),size = 1.5,stat = "identity",position="dodge",color="#9c6d6d",width =0.5)
+ geom_errorbar(aes(x='failure', y='counts',ymin='counts-error', ymax='counts+error',group = 'scenario2'),color="#4c4c4c",position=position_dodge(), size=1)
+ coord_flip()
+ scale_x_discrete(limits=q_list)
+ scale_fill_manual(values = ["#e81414","#ad144a","#4a271f"])#黄 "#d6e15e"
+ theme_dark()
+ ylim(0,num_station)
+ scale_y_continuous(limits=(0, num_station), breaks=break_y, labels=["0%", "20%", "40%", "60%", "80%","100%"])
+ labs(title=" ",x = '',y = '',fill = " ")
+ theme(
    aspect_ratio=3,
    dpi=300,
    panel_background = element_rect(fill="#fdfffd", alpha=.8,),
    legend_direction='vertically',
    legend_position=[0.75, 0.2],
    legend_background = element_rect(fill= "#F5F5F5",size = 3 ,color = "grey"  ),
    axis_text = element_text(size = 13,weight = "heavy"),
    legend_text = element_text(size = 13,weight = "heavy"),

)
)
# fig = qs.draw()
# fig.set_size_inches(10, 10, forward=True)
# # qs.save('figure/GIC_per_substation_graphic_his.png', height=10, width=8)
# fig.show()



import plotnine as p9
from matplotlib import gridspec
import matplotlib.pyplot as plt
from plotnine import data

# Create subplots using plotnine
# p1 = (p9.ggplot(data.diamonds, p9.aes(x='cut',y='carat'))+p9.geom_point())
# p2 = (p9.ggplot(data.diamonds, p9.aes(x='x',y='y'))+p9.geom_point())
parameters = {'axes.labelsize': 25,
          'axes.titlesize': 35}
plt.rcParams.update(parameters)
# Empty plotnine figure to place the subplots on. Needs junk data (for backend "copy" reasons).
fig = (p9.ggplot()+p9.geom_blank(data=tran)+p9.theme_void()).draw()
fig.tight_layout(h_pad=2)
# Create gridspec for adding subpanels to the blank figure
gs = gridspec.GridSpec(3,1)
ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[1,0])
ax3 = fig.add_subplot(gs[2,0])

# Add subplots to the figure
_ = qs1._draw_using_figure(fig, [ax1])
_ = qs2._draw_using_figure(fig, [ax2])
_ = qs3._draw_using_figure(fig, [ax3])




fig.subplots_adjust(left = 0.1)
fig.set_size_inches(5, 14, forward=True)
# fig.subplots_adjust(wspace=.3,hspace=0.7)
fig.savefig('figure/Probability_of_Failure_per_substation_right.png')
fig.show()

#尺寸调整
import matplotlib.pyplot as plt
from PIL import Image

image = Image.open('figure/Probability_of_Failure_per_substation_left.png')
resized_image = image.resize((905, 1400), Image.ANTIALIAS)
resized_image.save('figure/Probability_of_Failure_per_substation_left1.png')

#图片拼接

img1 = Image.open('figure/Probability_of_Failure_per_substation_left1.png')
img2 = Image.open('figure/Probability_of_Failure_per_substation_right.png')
size1, size2 = img1.size, img2.size

joint = Image.new("RGB", (size1[0] + size2[0], size1[1]))
loc1, loc2 = (0, 0), (size1[0], 0)

from PIL import Image, ImageDraw, ImageFont

# 打开图像
image = Image.open("figure/Probability_of_Failure_per_substation_left1.png")

# 创建绘制对象
draw = ImageDraw.Draw(image)

# 获取图像尺寸
width, height = image.size

# 指定方块左上角和右下角坐标
x1, y1 = 0, 0
x2, y2 = 80, 50

# 绘制方块
# draw.rectangle((x1, y1, x2, y2), fill="white")

# 加载TrueType字体
font = ImageFont.truetype("arial.ttf", 40)

# 绘制文本
text = "(a)"
color = "white"
text_width, text_height = draw.textsize(text, font=font)
x = x1 + (x2 - x1 - text_width) / 2
y = y1 + (y2 - y1 - text_height) / 2
draw.text((x, y), text, font=font, fill=color)

#右

# 打开图像
image2 = Image.open("figure/Probability_of_Failure_per_substation_right.png")

# 创建绘制对象
draw = ImageDraw.Draw(image2)

# 获取图像尺寸
width, height = image2.size

# 指定方块左上角和右下角坐标
x1, y1 = 0, 0
x2, y2 = 80, 50

# 绘制方块
# draw.rectangle((x1, y1, x2, y2), fill="white")

# 加载TrueType字体
font = ImageFont.truetype("arial.ttf", 40)

# 绘制文本
text = "(b)"
color = "black"
text_width, text_height = draw.textsize(text, font=font)
x = x1 + (x2 - x1 - text_width) / 2
y = y1 + (y2 - y1 - text_height) / 2
draw.text((x, y), text, font=font, fill=color)


joint.paste(image, loc1)
joint.paste(image2, loc2)
joint.save('figure/Probability_of_Failure_per_substation_Mean.png')
# joint.show()








