import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

on_h = pd.read_csv('./tmp/on_h.csv', index_col=0 ,encoding='utf-8')
train = pd.DataFrame(on_h.iloc[0:426, 0])
test = pd.DataFrame(on_h.iloc[426:, 0])
train['on_man'] = train['on_man'].astype(float)
# 定阶
bic_matrix = []  # bic矩阵，选择bic矩阵中最小值对应的行(p),列(q)
# 存在部分报错，所以用try来跳过报错
for p in range(11):
    tmp = []
    for q in range(5):
        try:
            tmp.append(sm.tsa.ARIMA(train, order=(p, 1, q)).fit().bic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)
bic_matrix = pd.DataFrame(bic_matrix)  # 从中可以找出最小值
p, q = bic_matrix.stack().idxmin()  # 先用stack展平，然后用idxmin找出最小值位置
print('BIC最小的p值和q值为：%s、%s' % (p, q))

model = sm.tsa.ARIMA(train, order=(p, 1, q)).fit()  # 建立ARIMA(p, 1, 1)模型
summary = model.summary()  # 给出一份模型报告
forecast = model.forecast(10)
print('10天的预测结果、标准误差和置信区间分别为：\n', forecast)

# pre = pd.DataFrame(forecast, columns = ['predict'])
pre = pd.DataFrame({'predict':forecast})
pre.index = test.index #如果索引不同将pre加到test中时会出错
test['pre'] = pre
plt.plot(test.index.values, test.on_man.values)
plt.plot(test.index.values, test.pre.values, linestyle=':')
plt.xticks(rotation = 45)
plt.legend(['true', 'predict'])
plt.title('compare with true and predict ')
plt.xlabel('date')
plt.ylabel('on_man')
plt.tight_layout()  # tight_layout()方法可以保证图像的完整度
plt.show()