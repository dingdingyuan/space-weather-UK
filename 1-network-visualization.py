import pyproj
import pandas as pd
radius = 0.6
#整合数据

#读取SUBSTATION数据
#lat lon
subtation = pd.read_csv("data/substation_info.csv")
#nodefrom,nodeto,voltage
connection = pd.read_csv("data/connections.csv")


# 创建WGS84坐标系对象
wgs84 = pyproj.Proj("+init=epsg:4326")

# 创建英国国家网格坐标系对象
ukgrid = pyproj.Proj("+init=epsg:27700")


df_sub_tran = pd.read_csv('data/df_sub_tran.csv')


def find_rows(df, col, n):
    # df 是 dataframe
    # col 是列名
    # n 是要寻找的整数
    mask = df[col].eq(n) # 创建一个布尔型的 mask
    return df[mask].index # 返回匹配行的索引






#新数据
subinfo = pd.read_csv('data/substation_info_UK_2022.csv')

condf = pd.read_csv('data/connections.csv_UK_2022')

subinfo.set_index('number', drop=True, inplace=True)

connection = condf
subtation = subinfo
number_list = [i for i in range(len(subinfo))]
subinfo["number"] = number_list

a = find_rows(subtation, "number", 5)
#data for network
#做一个新的电站network df
df_sub_net = pd.DataFrame(columns=['id', 'long', 'lat','voltage'])
for i in range(len(connection)):
    j = connection["nodefrom"][i]
    # 假设有一个WGS84坐标点（Longitude, Latitude）
    lon, lat = subtation["lon"][find_rows(subtation, "number", j)[0]],subtation["lat"][find_rows(subtation, "number", j)[0]]
    # 将其转换为英国国家网格坐标点（Easting, Northing）
    x, y = pyproj.transform(wgs84, ukgrid, lon, lat)
    df_sub_net = df_sub_net.append({'id': str(i), 'long':x, 'lat': y,'voltage':str(connection['voltage'][i])}, ignore_index=True)

    j = connection["nodeto"][i]
    # 假设有一个WGS84坐标点（Longitude, Latitude）
    lon, lat = subtation["lon"][find_rows(subtation, "number", j)[0]], subtation["lat"][find_rows(subtation, "number", j)[0]]
    # 将其转换为英国国家网格坐标点（Easting, Northing）
    x, y = pyproj.transform(wgs84, ukgrid, lon, lat)
    df_sub_net = df_sub_net.append({'id': str(i), 'long': x, 'lat': y, 'voltage': str(connection['voltage'][i])},
                                   ignore_index=True)

df_sub_net.to_csv('data/df_sub_net.csv', index=False)
df_sub_net = pd.read_csv('data/df_sub_net.csv')



import geopandas as gpd
import pandas as pd
from plotnine import *
from plotnine import ggplot, geom_map, aes, scale_fill_cmap, theme, labs
import plotnine as p9
from plotnine import geom_point
from plotnine import geom_point

############################################################
#### VISUALISE GRID (DOWN)
##
##        《图B》
##
############################################################

shp = gpd.read_file('data/all.shp')
tran = pd.read_csv("data/network.csv")
tran = df_sub_net
p = (
ggplot()
+geom_map(data=shp,color = "grey",fill="#F5F5F5", size = 0.3 ,alpha=0.8)
+geom_line(data=tran,mapping=aes(x = 'long', y = 'lat', group='id', colour='pd.Categorical(voltage)'), size =0.8, alpha=0.9)


+labs(title="(B) UK High Voltage\nNetwork",x='',y='')
# + coord_cartesian()
+ coord_equal(expand=False)
+ scale_colour_manual(name = "Line \nVoltage\n(kV)", values = ["#556b2f","#bced09","#FF0000"])
+ theme_dark()
+ theme(dpi=500,
    axis_text_x = element_blank(),
    axis_text_y = element_blank(),
    legend_text=element_text(weight='bold',va='top'),legend_title = element_text(hjust = 0,vjust = 0))
)
fig = p.draw()
fig.show()
p.save('figure/grid_structure.png', height=6, width=6)
# p.save('figure/grid_structure.eps',height=6, width=6,format='eps',dpi=500)




############################################################
#### VISUALISE DATA - EHV TRANSFORMER COUNT PER SUBSTATION (DOWN)
##
##        《图C》
##
############################################################
shp = gpd.read_file('data/all.shp')
tran = pd.read_csv("data/EHV_transformer_node_count.csv")
tran = df_sub_tran
from plotnine import geom_point

print(set(tran['transformer_count']))
tran['transformer_count1'] = tran['transformer_count'].astype('category')
tran['transformer_count1'] = tran['transformer_count1'].cat.reorder_categories([1, 2, 3,4,5,6,7],ordered=True)

p = (
ggplot()
+geom_map(data=shp,color = "grey",fill="#F5F5F5", size = 0.3 ,alpha=0.8)
+geom_point(data=tran,mapping=aes(x='Easting', y='Northing',size='pd.Categorical(transformer_count1)',color="pd.Categorical(transformer_count1)"), alpha=0.5)
+labs(title="(C) EHV Transformers Per\nSubstation (>270kV)",x='',y='')
+ coord_equal(expand=False)
# + scale_colour_manual(name = "EHV\nTransformer\nCount Per\nNode",values=["#6495ED","#FF8000","#FF0000"],labels = ['1', '2', '3'])
# + scale_size_manual(name = "EHV\nTransformer\nCount Per\nNode",values=[2, 4],labels = ['1', '2', '3'],na_value = 6)#,na_value=True,na_translate=True,guide=True

# "#696969","#6495ED","#00FF80","#80FF00","#FFD700","#FF8000","#FF0000"
+ scale_colour_manual(name = "EHV\nTransformer\nCount Per\nNode",values=["#696969","#6495ED","#00FF80","#80FF00","#FFD700","#FF8000","#FF0000"],labels = ['1', '2', '3','4','5','6','7'])
+ scale_size_manual(name = "EHV\nTransformer\nCount Per\nNode",values=[2, 3,4,5,6,7],labels = ['1', '2', '3','4','5','6','7'],na_value = 8)#,na_value=True,na_translate=True,guide=True
+ theme_dark()
+ theme(dpi=500,
    axis_text_x = element_blank(),
    axis_text_y = element_blank(),
    #aspect_ratio=1   # height:width
    axis_text = p9.themes.element_text(size = 5, color = "#999999"),
    legend_text=element_text(hjust = 1),
    axis_title = element_text(hjust = 1,vjust = 1),
    title = element_text(hjust = 0.5,vjust = 0),
    legend_title = element_text(hjust = 0,vjust = 0))
)
fig = p.draw()
fig.show()
p.save('figure/EHV_transformer_count_per_substation.png', height=6, width=6)
# p.save('figure/EHV_transformer_count_per_substation.eps',height=6, width=6,format='eps',dpi=500)

import pandas as pd
df = pd.read_csv('data/df_sub_popu.csv')
#
# print(df_sub_popu)



import geopandas as gpd
import pandas as pd
from plotnine import *
from plotnine import ggplot, geom_map, aes, scale_fill_cmap, theme, labs
import plotnine as p9
from plotnine import geom_point

############################################################
#### VISUALISE DATA - POPULATION PER SUBSTATION (DOWN)
##
##        《图A》
##
############################################################

shp = gpd.read_file('E:\\2023夏\\UKporject3.2\\1-netwrork-visualization-data\\all.shp')
tran = pd.read_csv("E:\\2023夏\\UKporject3.2\\1-netwrork-visualization-data\\substation_results_population.csv")

#删列测试
# 删除第一列（列名为'a'）
tran = tran.drop('Site.Code', axis=1)
tran = tran.drop('Unnamed: 0', axis=1)
len_tran = len(tran)
print(tran)
print(df)
list1 = set(df["Population"])
print(list1)
tran = df
# for i in range(len(df)):
#     tran = tran.append({'Population':df["Population"][i], 'Easting': df["Easting"][i], 'Northing': df['Northing'][i]}, ignore_index=True)
# tran.drop(df.head(260).index, inplace=True)

from plotnine import geom_point


# tran['Population1'] = tran['Population'].astype('category')
# tran['Population1'] = tran['Population1'].cat.reorder_categories(["<0.15", "0.15-0.3", "0.3-0.45", "0.45-0.6","0.6-0.75", "0.75-0.9",">0.9"],ordered=True)

# {'0.45-0.6', '0.15-0.3', '<0.15', '0.3-0.45'}
tran['Population1'] = tran['Population'].astype('category')
tran['Population1'] = tran['Population1'].cat.reorder_categories(["<0.15", "0.15-0.3", "0.3-0.45", "0.45-0.6"],ordered=True)

p = (
ggplot()
+geom_map(data=shp,color = "grey",fill="#F5F5F5", size = 0.3 ,alpha=0.8)
+geom_point(data=tran,mapping=aes(x='Easting', y='Northing',size='pd.Categorical(Population1)',color="pd.Categorical(Population1)"), alpha=0.5)


+labs(title="(A) Population Served\nPer Substation",x='',y='')

+ coord_equal(expand=False)
# + scale_colour_manual(name = "Population\nPer Node\n(Million)",values=["#696969","#6495ED","#00FF80","#80FF00","#FFD700","#FF8000","#FF0000"],labels = ["<0.15", "0.15-0.3", "0.3-0.45", "0.45-0.6",
#                            "0.6-0.75", "0.75-0.9",">0.9"])
# + scale_size_manual(name = "Population\nPer Node\n(Million)",values=[1, 2, 3, 4, 5, 6],labels = ["<0.15", "0.15-0.3", "0.3-0.45", "0.45-0.6",
#                                  "0.6-0.75", "0.75-0.9",">0.9"],na_value=7)#,na_value=True,na_translate=True,guide=True
+ scale_colour_manual(name = "Population\nPer Node\n(Million)",values=["#6495ED","#00FF80","#80FF00","#FFD700"],labels = ["<0.15", "0.15-0.3", "0.3-0.45", "0.45-0.6"
                        ])
+ scale_size_manual(name = "Population\nPer Node\n(Million)",values=[2, 4, 6],labels = ["<0.15", "0.15-0.3", "0.3-0.45", "0.45-0.6"
                                 ],na_value=8)#,na_value=True,na_translate=True,guide=True


+ theme_dark()
+ theme(
    dpi=500,
    axis_text_x = element_blank(),
    axis_text_y = element_blank(),
    #aspect_ratio=1   # height:width
    axis_text = p9.themes.element_text(size = 5, color = "#999999"),
    legend_text=element_text(hjust = 1),
    axis_title = element_text(hjust = 1,vjust = 1),
    title = element_text(hjust = 0.5,vjust = 0),
    legend_title = element_text(hjust = 0,vjust = 0)
)
)
fig = p.draw() #
fig.show()
p.save('figure/population_per_substation.png', height=6, width=6)
# p.save('figure/population_per_substation.eps',height=6, width=6,format='eps',dpi=500)