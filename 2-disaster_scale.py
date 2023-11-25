import pandas as pd

data1 = pd.read_csv(r'data\max_UK_GIC.csv', index_col=0)
data2 = pd.read_csv(r'data\march1989_UK_GIC.csv', index_col=0)



disaster_in_str = ['11years', '22years', '33years',
                       '55years', '110years','1000years',
                       '10000years','100000years','1000000years']

disaster_name = ['1989-11.csv', '1989-22.csv', '1989-33.csv', '1989-55.csv',
                 '1989-110.csv', '1989-1000.csv', '1989-10000.csv',
                 '1989-100000.csv', '1989-1000000.csv']

node_number = 387
level_number = 9


max1989 = max(data1['Mar-89'])
# print(data2.iloc[0:,1])
for i in range(level_number):
    data2 = pd.read_csv(r'data\march1989_UK_GIC.csv',index_col=0)
    max1 = max(data1[disaster_in_str[i]])
    d = max1/max1989
    for n in range(node_number):
        data2.iloc[0:, n] = data2.iloc[0:, n]*d
    path = r"data/" + disaster_name[i]
    data2.to_csv(path)

