# 预处理 201501-201603这段时间的铁路信息
# 需求：从这些文件中获得所需的铁路信息
# 获取'on_station', 'on_man', 'on_time','off_man', 'off_time', 'date', 'train'
import os
from itertools import chain
import pandas as pd
import re
from redeal import Deal_Fun

path = './data/201501-201603'
filename = os.listdir(path)  # 得到文件夹下的所有文件名称
n_filename = len(filename)  # n_filename=15
datalist = []
date = []
for i in range(n_filename):
    name = './data/201501-201603/' + filename[i]
    datalist.append(['./data/201501-201603/' + filename[i] + '/' + j for j in os.listdir(name)])
    date.append(len(datalist[i]))
# append 会把整个列表作为一个元素添加进去，所以 datalist 自然成为由多个列表组成的二维列表。
filedata = list(chain.from_iterable(datalist))  # 将二维列表转换为一维列表
n_file = sum(date)
SaveFile_Name = './tmp/Station.csv'  # 数据合并后要保存的文件名（Station表合并）

Deal_Fun(n_file, filedata, SaveFile_Name)

Train_Station = pd.read_csv('./tmp/Station.csv',header=None, encoding='utf-8')
Train_Station.columns = ['on_station', 'on_man', 'on_time','off_man', 'off_time', 'date', 'Station']
Train_Station.fillna(value=0, inplace=True)  # 处理nan值

# 处理之前设置为0.1的缺省值重新设置为0
for i in range(len(Train_Station)):
    for j in range(len(Train_Station.iloc[0, :])):
        if Train_Station.iloc[i, j] == '0.1':
            Train_Station.iloc[i, j] = 0
# Train_Station['date'] 每个元素中提取 8 位数字，并格式化成 YYYY-MM-DD
s_date = [re.findall('[0-9]+', i)[0][0:4] +
          '-' + re.findall('[0-9]+', i)[0][4:6] +
          '-' + re.findall('[0-9]+', i)[0][6:8]
          for i in Train_Station.loc[:, 'date']]
Train_Station.loc[:, 'date'] = s_date

# 部分数据为空格，将其替换为0
ind_on = [i for i in Train_Station.index if Train_Station.loc[i, 'on_man'] == ' ']
ind_off = [i for i in Train_Station.index if Train_Station.loc[i, 'off_man'] == ' ']
Train_Station.loc[ind_on, 'on_man'] = 0
Train_Station.loc[ind_off, 'off_man'] = 0
Train_Station['on_man'] = Train_Station['on_man'].astype(float)
Train_Station['off_man'] = Train_Station['off_man'].astype(float)

Train_Station.to_csv('./tmp/Train_Station.csv', encoding='utf-8')
Train_Station = pd.read_csv('./tmp/Train_Station.csv', index_col=0, encoding='utf-8')
