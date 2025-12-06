import pandas as pd
import matplotlib.pyplot as plt

Train_Station = pd.read_csv('./tmp/Train_Station.csv', index_col=0, encoding='utf-8')
Train_ST111_01 = Train_Station[Train_Station.iloc[:, 0] == 'ST111-01']
# 上车客流分析
On_t = Train_ST111_01.iloc[:, 1:3] # python切片左避右开原则，故第1-2列
On_t.index = range(len(On_t))
# 时间取整点
for i in range(len(On_t)):
    if On_t.iloc[i, 1] != 0:
        On_t.iloc[i, 1] = int(On_t.iloc[i, 1][0:2]) # 字符串切片
on_mean_t = On_t.groupby('on_time')['on_man'].mean()  # 分组并求均值
on_mean_t.plot(kind='bar', title='every time people on', color='blue')
plt.xticks(rotation=0)
plt.ylabel('on of mans')
plt.xlabel('time')
plt.show()

# 下车客流分析
Off_t = Train_ST111_01.iloc[:, 3:5]
Off_t.index = range(len(Off_t))
for i in range(len(Off_t)):
    if Off_t.iloc[i, 1] != 0:
        Off_t.iloc[i, 1] = int(Off_t.iloc[i, 1][0:2])
off_mean_t = Off_t.groupby('off_time')['off_man'].mean()  # 分组并求均值
off_mean_t.plot(kind='bar', color='red', title='every time people off')
plt.xticks(rotation=0)
plt.ylabel('off of mans')
plt.xlabel('time')
plt.show()


