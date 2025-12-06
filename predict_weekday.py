# 剔除节假日及前一天后的时序图
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import itertools
import numpy as np
import statsmodels.api as sm
import matplotlib.ticker as ticker

on_h = pd.read_csv('./tmp/on_h.csv', index_col=0 ,encoding='utf-8')
new_h = on_h  # 存放节假日更新的数据
new_h.index = range(len(new_h))
for i in range(1, len(new_h)):
    if new_h.iloc[i, 2] == '小长假' :
        new_h.iloc[i-1, 2] = '小长假'
new_nh = new_h[new_h.iloc[:,2] != '小长假']  # 剔除节假日及其前一天
# print(new_nh.columns)
# print(new_nh.head())
# print(type(new_nh['date.1']))
# print(new_nh['date.1'].shape)

plt.plot(new_nh['date.1'], new_nh['on_man'],color='green')
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(70))
plt.xticks(rotation = 45)
plt.title('Excluding holidays in ST111-01 station passenger flow date')
plt.legend(['on_man'], loc=2)
plt.xlabel('date')
plt.ylabel('passenger flow')
plt.tight_layout()  # tight_layout()方法可以保证图像的完整度
# plt.savefig('./tmp/9.png', dpi=1080)
plt.show()

new_nh.index = range(len(new_nh))
# 前378行作为训练集，372后面的作为测试集合
train1 = pd.DataFrame(new_nh.iloc[0:378, 0])
test1 = pd.DataFrame(new_nh.iloc[372:, 0])
# 设置 ARIMA时间序列模型预测 参数组合
p = q = range(4) # ARIMA 模型的自回归阶数、移动平均阶数
d = range(2) # 差分阶数
# 生成非季节性ARIMA模型的参数组合列表
pdq = list(itertools.product(p, d, q))

seasonal_pdq = [(x[0], x[1], x[2], 7)for x in list(itertools.product(p, d, q))]
print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))
# 使用SARIMAX 模型训练
warnings.filterwarnings("ignore")  # specify to ignore warning messages
sa =[]
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(train1,order=param, seasonal_order=param_seasonal, enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            print('ARIMA{}x{}7 - AIC:{}'.format(param, param_seasonal, results.aic))
            sa.append(param)
            sa.append(param_seasonal)
            sa.append(results.aic)
        except:
            continue
# 找出最优参数
AIC = [i for i in sa if type(i) == np.float64]
AIC_min = min(AIC)
for i in np.arange(2,len(sa),3):
    if sa[i] == min(AIC):
        param = sa[i-2]
        param_seasonal = sa[i-1]
mod = sm.tsa.statespace.SARIMAX(train1,order=(param), seasonal_order=(param_seasonal),enforce_stationarity=False, enforce_invertibility=False)
print('模型最终定阶为：', (param, param_seasonal))
results = mod.fit()
print(results.summary().tables[1])
fig = plt.figure(figsize=(15, 12))
results.plot_diagnostics(figsize=(15, 12), fig=fig)
plt.show()

# 模型预测
pre_10 = results.predict(start=372, end=381,dynamic=True)
out_pre = pd.DataFrame(np.zeros([10,3]),columns = ['real', 'pre', 'error'])
out_pre['real'] = list(test1['on_man'])
out_pre['pre'] = list(pre_10)
# 计算相对误差
error_seasonal = (out_pre.loc[:, 'pre']-out_pre.loc[:,'real'])/out_pre.loc[:,'real']
# 平均相对误差
error_mean = abs(error_seasonal).mean()
print('预测平均相对误差为：', error_mean)
