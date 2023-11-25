"""
UK Space Weather Analysis (python)
————Figures

author：王贤
time：2022.11.21



This program draws the sub-graphs of figure.2
Figure Left and Figure Right


"""


import geopandas as gpd
from plotnine import *
from plotnine import ggplot, geom_map, aes, scale_fill_cmap, theme, labs

shp = gpd.read_file('data/all.shp')
# tran = pd.read_csv("GIC_per_substation.csv")

from plotnine import geom_point
import plotnine as p9

######################
import pandas as pd
import numpy as np

df=pd.read_csv("data/max_uk_gic8.28.csv")
# print(df.head())



dic = {
    "TargetID":[],
    "scenario": [],  # 列表
    "current": [],  # 数组
    "Easting": [],
    "Northing": [],
}  # 元组
data = pd.DataFrame(dic)  # 创建Dataframe

# data.loc[0]=[ 'Mango', 4, 'No' ]
list_scenario=["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"]
print(data)
list_current = ["0-25A",'25-50A','50-75A','75-100A','100-125A','125-150A','150-175A','>175A']
n=0
for i in range(len(df)):
    for j in range(len(list_scenario)):
        current_level = int(df.iloc[i][4+j]  // 25)
        if current_level >= 7:
            current_level = 7
        data.loc[n] = [df['node_number'][i],list_scenario[j],list_current[current_level],df['longitude'][i],df['latitude'][i]]
        n = n+1

print(data)

import numpy as np
import pandas as pd
from pyproj import Proj, transform
ukgrid = "+init=epsg:27700"
latlong = "+init=epsg:4326"

data['Easting'], data['Northing'] = transform(Proj(latlong, preserve_units=False),
                                                          Proj(ukgrid, preserve_units=False),
                                                          data['Easting'], data['Northing'])

print(data)
###############


tran = data





tran['scenario1'] = tran['scenario'].astype('category')
print(tran['scenario1'])

tran['scenario1'] = tran['scenario1'].cat.reorder_categories(["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"],ordered=True)

tran['scenario1'] = tran['scenario'].astype('category')
print(tran['scenario1'])

tran['scenario1'] = tran['scenario1'].cat.reorder_categories(["1-in-11","1-in-22","1-in-33","1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"],ordered=True)





# print(tran[tran['scenario'] == "1-in-33"]['failure'].value_counts())


#地图

tran['current1'] = tran['current'].astype('category')
tran['current1'] = tran['current1'].cat.reorder_categories(list_current,ordered=True)

shp = gpd.read_file('data/all.shp')

list_color = ["#999999","#666666","#80FF00","#00FF80","#FFD700","#FF8000","brown","#FF0000"]
p = (
ggplot()
+geom_map(data=shp,color = "grey",fill="#F5F5F5", size = 0.3 ,alpha=0.8)
+geom_point(data=tran,mapping=aes(x='Easting', y='Northing', size='pd.Categorical(current1)',
                                              colour='pd.Categorical(current1)'), alpha=0.3)
+ labs(title="",x = '',y = '')
+ coord_equal(expand=False)
+ facet_wrap("scenario1",
             nrow=3 ,
        # change the number of columns
             )
# +guides(fill = guide_legend(reverse = False))
# ["#999999","#666666","#80FF00","#00FF80","#FFD700","#FF8000","brown","#FF0000"]

+ scale_colour_manual(name = "  ",values=list_color,labels = list_current)
+ scale_size_manual(name = "  ",values=[1, 2, 3, 4, 5, 6,7 ],labels = list_current, na_value = 7)
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
    legend_position=[0.335, 0.829],
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
p.save('figure/GIC_left.png', height=14, width=14)




# 处理dataframe
# 柱形图

num_station = 387
break_y = [0 * num_station/5 , 1 * num_station/5, 2 * num_station/5, 3 * num_station/5, 4 * num_station/5,5 * num_station/5]



tran = data
tran["current"] = tran["current"].replace('150-175A', '>150A', regex=True)
tran["current"] = tran["current"].replace('> 175A', '>150A', regex=True)







# current_list = ['0-25', '25-50', '50-75', '75-100', '100-125',  '125-150', '150-175','> 175']
current_list = ['0-25A', '25-50A', '50-75A', '75-100A', '100-125A',  '125-150A', '>150A']
tran1 = tran[(tran['scenario'] == '1-in-11') |(tran['scenario'] == '1-in-22') |(tran['scenario'] == '1-in-33')]
tran2 = tran[(tran['scenario'] == '1-in-55') |(tran['scenario'] == '1-in-110') |(tran['scenario'] == '1-in-1,000')]
tran3 = tran[(tran['scenario'] == '1-in-10,000') |(tran['scenario'] == '1-in-100,000') |(tran['scenario'] == '1-in-1,000,000')]
alpha = 0.7

tran1['scenario2'] = tran1['scenario'].astype('category')
# print(tran['scenario1'])
tran1['scenario2'] = tran1['scenario2'].cat.reorder_categories(["1-in-11","1-in-22","1-in-33"],ordered=True)
# "1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"


tran2['scenario2'] = tran2['scenario'].astype('category')
# print(tran['scenario1'])
tran2['scenario2'] = tran2['scenario2'].cat.reorder_categories(["1-in-55","1-in-110","1-in-1,000"],ordered=True)
# "1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"


tran3['scenario2'] = tran3['scenario'].astype('category')
# print(tran['scenario1'])
tran3['scenario2'] = tran3['scenario2'].cat.reorder_categories(["1-in-10,000","1-in-100,000","1-in-1,000,000"],ordered=True)
# "1-in-55","1-in-110","1-in-1,000","1-in-10,000","1-in-100,000","1-in-1,000,000"

top = num_station/5
qs1 = (
ggplot()
# + geom_bar(tran1, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20)
+ geom_bar(tran1, aes(x='current', y=after_stat('count'),fill='scenario2',),size = 1.5,color="#9c6d6d",width =0.5,position="dodge")
# + geom_bar(tran22, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
# + geom_bar(tran33, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha,position="dodge")
+ coord_flip()
+ scale_x_discrete(limits=current_list)
# + facet_wrap('scenario1') # facet wrap
+ scale_fill_manual(values = ["#e81414","#ad144a","#4a271f"]) #"#999999","#666666","#80FF00","#00FF80","#FFCC00","#FF8000","#FF0000","brown"
# + geom_text(aes(x='current',
#               y=after_stat('count'),
#               label=after_stat('count')),
#               color = 'black',
#               size=10,
#               nudge_y=200,
#               nudge_x=0)
# + geom_text(aes(label=after_stat('count')), stat='count',nudge_y=50)
# + facet_wrap('scenario1') # facet wrap
+ theme_dark()
+ guides(
    nrow = 3,ncol = 1
 )
+ ylim(0,num_station)
# + xlab("A")
+ scale_y_continuous(limits=(0, num_station ), breaks=[0,top,top*2,top*3,top*4,top*5], labels=["0%", "20%", "40%", "60%", "80%","100%"])
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
ggplot()
+ geom_bar(tran2, aes(x='current', y=after_stat('count'),fill='scenario2'),size = 1.5,color="#9c6d6d",width =0.5,position="dodge")
# + geom_bar(tran1, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20)
# + geom_bar(tran55, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
# + geom_bar(tran110, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
# + geom_bar(tran1k, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
+ coord_flip()
+ scale_x_discrete(limits=current_list)
# + facet_wrap('scenario1') # facet wrap
# + scale_fill_manual(values = ["#999999","#666666","#80FF00","#00FF80","#FFCC00","#FF8000","brown","#FF0000"]) #"#999999","#666666","#80FF00","#00FF80","#FFCC00","#FF8000","#FF0000","brown"
+ scale_fill_manual(values = ["#e81414","#ad144a","#4a271f"]) #"#3621b2","#0c8993","#24c578"
# + geom_text(aes(x='current',
#               y=after_stat('count'),
#               label=after_stat('count')),
#               color = 'black',
#               size=10,
#               nudge_y=200,
#               nudge_x=0)
# + geom_text(aes(label=after_stat('count')), stat='count',nudge_y=50)
# + facet_wrap('scenario1') # facet wrap
+ theme_dark()
+ ylim(0,num_station )
+ scale_y_continuous(limits=(0, num_station ), breaks=break_y, labels=["0%", "20%", "40%", "60%", "80%","100%"])
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

qs3 = (
ggplot()
# + geom_bar(tran1, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20)
+ geom_bar(tran3, aes(x='current', y=after_stat('count'),fill='scenario2'),size = 1.5,color="#9c6d6d",width =0.5,position="dodge")
# + geom_bar(tran10k, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
# + geom_bar(tran100k, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
# + geom_bar(tran1kk, aes(x='current', y=after_stat('count'),fill='scenario1'),size=20,alpha =alpha)
+ coord_flip()
+ scale_x_discrete(limits=current_list)
# + facet_wrap('scenario1') # facet wrap
# + scale_fill_manual(values = ["#999999","#666666","#80FF00","#00FF80","#FFCC00","#FF8000","brown","#FF0000"]) #"#999999","#666666","#80FF00","#00FF80","#FFCC00","#FF8000","#FF0000","brown"
+ scale_fill_manual(values = ["#e81414","#ad144a","#4a271f"])#黄 "#d6e15e"
# + geom_text(aes(x='current',
#               y=after_stat('count'),
#               label=after_stat('count')),
#               color = 'black',
#               size=10,
#               nudge_y=200,
#               nudge_x=0)
# + geom_text(aes(label=after_stat('count')),position=position_dodge(width=0.9), stat='count',nudge_y=50)
# + facet_wrap('scenario1') # facet wrap
+ theme_dark()
+ ylim(0,num_station )
+ scale_y_continuous(limits=(0, num_station ), breaks=break_y, labels=["0%", "20%", "40%", "60%", "80%","100%"])
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




fig.subplots_adjust(left = 0.25)
fig.set_size_inches(5, 14, forward=True)
# fig.subplots_adjust(wspace=.3,hspace=0.7)
fig.savefig('figure/GIC_right.png')
fig.show()

#尺寸调整
import matplotlib.pyplot as plt
from PIL import Image

image = Image.open('figure/GIC_left.png')
resized_image = image.resize((905, 1400), Image.ANTIALIAS)
resized_image.save('figure/GIC_left_2.png')

#图片拼接

img1 = Image.open('figure/GIC_left_2.png')
img2 = Image.open('figure/GIC_right.png')
size1, size2 = img1.size, img2.size

joint = Image.new("RGB", (size1[0] + size2[0], size1[1]))
loc1, loc2 = (0, 0), (size1[0], 0)

# from PIL import Image, ImageDraw, ImageFont
# drawImg = ImageDraw.Draw(img1)  # 创建一个绘画对象，在img上面画
# font = ImageFont.truetype("arial.ttf", 40)  # ImageFont对象
# # print(img.size)
# drawImg.text((20, 5), "(a)", font,fill = "white") # 确定好坐标不能超了！！！
# # img1.save("figure/GIC_left_2.png")
#
# drawImg = ImageDraw.Draw(img2)  # 创建一个绘画对象，在img上面画
# font = ImageFont.truetype("arial.ttf", 40)  # ImageFont对象
# # print(img.size)
# drawImg.text((20, 5), "(b)", (0, 0, 0), font)  # 确定好坐标不能超了！！！
# # img1.save("figure/GIC_right.png")



from PIL import Image, ImageDraw, ImageFont

# 打开图像
image = Image.open("figure/GIC_left_2.png")

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
image2 = Image.open("figure/GIC_right.png")

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
# 保存图像
# image.save("output.jpg")



joint.paste(image, loc1)
joint.paste(image2, loc2)
joint.save('figure/GIC_distributed.png')
joint.show()

