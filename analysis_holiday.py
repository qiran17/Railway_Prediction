import pandas as pd
import matplotlib.pyplot as plt
import re

Train_Station = pd.read_csv('./tmp/Train_Station.csv', index_col=0, encoding='utf-8')  # 必须index_col=0把第0列作为索引
holiday = open('./data/2015-2016节假日.csv', encoding='utf-8')
holiday = pd.read_csv(holiday)
for i in range(len(holiday)):
    s = re.findall('[0-9]+', holiday.iloc[i, 0])
    l = s[0]
    # 构造 YYYY-MM-DD
    if len(s[1]) < 2:
        l = l + '-' + '0' + s[1]
    else:
        l = l + '-' + s[1]
    if len(s[2]) < 2:
        l = l + '-' + '0' + s[2]
    else:
        l = l + '-' + s[2]
    holiday.iloc[i, 0] = l
holiday.to_csv('./tmp/holiday.csv', encoding='utf-8')
Train_ST111_01 = Train_Station[Train_Station.iloc[:, 0] == 'ST111-01']
on_h = Train_ST111_01.groupby('date')['on_man'].sum()  # on_h.index = 'date'
on_h = pd.DataFrame(on_h)
on_h['date'] = 0
on_h['holiday'] = 0
# 添加日期和类型（工作日或者小长假）
for i in range(len(holiday)):
    for j in range(len(on_h)):
        if holiday.iloc[i, 0] == on_h.index[j]:
            on_h.loc[on_h.index[j], 'holiday'] = holiday.iloc[i, 1]
            on_h.loc[on_h.index[j], 'date'] = holiday.iloc[i, 0]
# on_h : [{date},'on_man','date','holiday']
# 节假日影响图
fig = plt.figure(figsize=(20, 12))
ax = fig.add_subplot(1, 1, 1)
for i in range(len(on_h) - 2):
    for j in range(i + 1, len(on_h) - 1):
        if on_h.iloc[i, 2] == on_h.iloc[j, 2] and on_h.iloc[i, 2] != on_h.iloc[j + 1, 2]: # 找出每段节假日的起点 i 与终点 j
            if on_h.iloc[i, 2] == '小长假':
                ax.scatter(on_h.iloc[i, 1], on_h.iloc[i, 0], color='red', linewidth=5)
                ax.plot(on_h.iloc[i:j + 1, 1].values, on_h.iloc[i:j + 1, 0].values, color='black')
            else:
                ax.plot(on_h.iloc[i:j + 1, 1].values, on_h.iloc[i:j + 1, 0].values, color='black')
on_h.to_csv('./tmp/on_h.csv', encoding='utf-8')
plt.xlabel('DATE')
plt.ylabel('on_man')
plt.legend(['point-holiday', 'black line-all date'], loc=8)
plt.title('customer_flow change in holiday')
plt.xticks((0, 50, 100, 150, 200, 250, 300, 350, 400), rotation=30)
plt.tight_layout()
plt.rcParams.update({'font.size': 33})
plt.show()
