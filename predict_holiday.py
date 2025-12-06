# 节假日客流规律
# 由于之前步骤对on_h有修改，所以此处重新载入
import pandas as pd
import matplotlib.pyplot as plt
import math

holiday = pd.read_csv('./tmp/holiday.csv', index_col=0 ,encoding = 'utf-8')
Train_Station = pd.read_csv('./tmp/Train_Station.csv', index_col=0 ,encoding='utf-8')
Train_ST111_01 = Train_Station[Train_Station.iloc[:, 0] == 'ST111-01']
on_h = Train_ST111_01.groupby('date')['on_man'].sum()
on_h = pd.DataFrame(on_h)
on_h['date'] = 0
on_h['holiday'] = 0
# 添加日期和类型（工作日或者小长假）
for i in range(len(holiday)):
    for j in range(len(on_h)):
        if holiday.iloc[i,0] == on_h.index[j]:
            on_h.loc[on_h.index[j], 'holiday'] = holiday.iloc[i,1]
            on_h.loc[on_h.index[j], 'date'] = holiday.iloc[i,0]
# 2015春节
fig = plt.figure(figsize=(12, 6))  # 设置画布
ax = fig.add_subplot(1, 1, 1)
ax.plot(on_h.loc['2015-01-19':'2015-02-18', 'on_man'], color = 'blue')
ax.plot(on_h.loc['2015-02-18':'2015-02-25', 'on_man'], color = 'red', linestyle=':')
ax.plot(on_h.loc['2015-02-25':'2015-03-01', 'on_man'], color = 'blue')
plt.xlabel('date')
plt.ylabel('on_man')
plt.title('2015 Spring Festival passenger flow')
plt.legend(['workday','holiday'])
plt.xticks(rotation = 45)
plt.show()

# 2015劳动节
fig1 = plt.figure(figsize=(12, 6))  # 设置画布
ax1 = fig1.add_subplot(1, 1, 1)
ax1.plot(on_h.loc['2015-04-27':'2015-05-01', 'on_man'], color = 'blue')
ax1.plot(on_h.loc['2015-05-01':'2015-05-04', 'on_man'], color = 'red', linestyle=':')
ax1.plot(on_h.loc['2015-05-04':'2015-05-11', 'on_man'], color = 'blue')
plt.xlabel('date')
plt.ylabel('on_man')
plt.title('WUYI passenger flow')
plt.legend(['workday','holiday'])
plt.xticks(rotation = 45)
plt.show()

# 国庆和中秋
fig2 = plt.figure(figsize=(12, 6))  # 设置画布
ax2 = fig2.add_subplot(1, 1, 1)
ax2.plot(on_h.loc['2015-09-21':'2015-09-26', 'on_man'],color = 'blue')
ax2.plot(on_h.loc['2015-09-26':'2015-09-28', 'on_man'],color = 'red', linestyle=':')
ax2.plot(on_h.loc['2015-09-28':'2015-09-30', 'on_man'],color = 'blue')
ax2.plot(on_h.loc['2015-09-30':'2015-10-08', 'on_man'],color = 'red', linestyle=':')
ax2.plot(on_h.loc['2015-10-08':'2015-10-12', 'on_man'],color = 'blue')
plt.xlabel('date')
plt.ylabel('on_man')
plt.title('ZHONGQIU and GUOQING passenger flow')
plt.legend(['workday', 'holiday'])
plt.xticks(rotation = 45)
plt.show()

# 2015和2016春节客流量比较
compare = pd.DataFrame(on_h.loc['2015-02-05':'2015-02-26', 'on_man'])
compare['2016'] = list(on_h.loc['2016-01-25':'2016-02-15', 'on_man'])
compare.columns = ['2015', '2016']
compare.index = range(len(compare))
plt.plot(compare.index, compare['2015'], linestyle=':')
plt.plot(compare.index, compare['2016'])
plt.legend(['2015', '2016'])
plt.xlabel('date')
plt.ylabel('passenger flow')
plt.title('2015 and 2016 Spring Festival passenger flow')

# 2015春节节假日波动系数
M = on_h.loc['2015-01-01':'2015-02-17']
M = M[M.loc[:,'holiday'] != '小长假']
M1 = on_h.loc['2015-01-01':'2015-02-07']
M1 = M1[M1.loc[:,'holiday'] != '小长假']
B_coef = []
# 春节前10天
for i in on_h.loc['2015-02-08':'2015-02-17',:].index:
    B_coef.append('%.2f' % (on_h.loc[i, 'on_man']/math.ceil(M1.iloc[-30:,0].mean())))
# 春节及春节后两天
for i in on_h.loc['2015-02-18':'2015-02-26',:].index:
    B_coef.append('%.2f' % (on_h.loc[i, 'on_man']/math.ceil(M.iloc[-30:,0].mean())))
# 将列表转为 DataFrame, 列名为 'on_man',转成 float 类型，以便绘图和计算
B_coef = pd.DataFrame(B_coef)
B_coef.columns = ['on_man']
B_coef[u'on_man'] = B_coef[u'on_man'].astype(float)
fig3 = plt.figure(figsize=(8,6))  # 设置画布
ax3 = fig3.add_subplot(1, 1, 1)
ax3.plot(B_coef.iloc[:,0], color='blue')
plt.xlabel('Index')
plt.ylabel('coefficient')
plt.title('2015 Spring Festival holiday fluctuation coefficient')
# 设置数字标签
for a, b in zip(B_coef.index, B_coef.iloc[:, 0]):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
plt.legend()
plt.show()

# 根据假期客流量的相似性，构造2015年春节的客流量的波动系数来预测2016年春节客流量
MM = on_h.loc['2015-01-01':'2016-02-06',:]
MM = MM[MM.loc[:, 'holiday'] != '小长假']
MM_mean = math.ceil(MM.iloc[-30:,0].mean())
MM1 = on_h.loc['2015-01-01':'2016-01-27',:]
MM1 = MM1[MM1.loc[:, 'holiday'] != '小长假']
MM1_mean = math.ceil(MM1.iloc[-30:,0].mean())

pre_2016_b = B_coef.iloc[0:10, 0] * MM1_mean
pre_2016_a = B_coef.iloc[10:, 0] * MM_mean
pre_2016 = pd.DataFrame(on_h.loc['2016-01-28':'2016-02-15', 'on_man'])
pre_2016['pre'] = 0
pre_2016.iloc[0:10, 1] = list(pre_2016_b)
pre_2016.iloc[10:, 1] = list(pre_2016_a)
pre_2016.columns=['real', 'pre']
plt.plot(pre_2016.index, pre_2016.real)
plt.plot(pre_2016.index, pre_2016.pre, linestyle=':')
plt.xticks(rotation=45)
plt.legend(['real', 'pre'])
plt.xlabel('date')
plt.ylabel('passenger flow')
plt.title('predict 2016 Spring Festival passenger flow')
plt.show()

# 计算相对误差
error_pre = (pre_2016.loc[:, 'pre'] - pre_2016.loc[:, 'real'])/pre_2016.loc[:, 'real']
# 平均相对误差
error_pre_mean = abs(error_pre).mean()
print('预测的平均相对误差为：', error_pre_mean)
