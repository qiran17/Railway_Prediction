import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller as ADF
import matplotlib.ticker as ticker

on_h = pd.read_csv('./tmp/on_h.csv', index_col=0 ,encoding='utf-8')
train = pd.DataFrame(on_h.iloc[0:426, 0])
test = pd.DataFrame(on_h.iloc[426:, 0])
#train.plot(title = '训练集时序图')  # 画训练集时序图
x = train.index.values
y = train.on_man.values
fig, ax = plt.subplots(1,1)
ax.plot(x, y)
ticker_spacing = 70
ax.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
plt.xticks(rotation = 45)
plt.xlabel('date')
plt.ylabel('customer flow')
plt.title('train_set time fig')
plt.tight_layout()  # tight_layout()方法可以保证图像的完整度
plt.show()

plot_acf(train,lags=400)
plt.xlabel('date index')
plt.ylabel('Autocorrelation')
plt.title('train_set autocorrelate fig')
plt.tight_layout()
plt.show()  # 画训练集自相关图

print('原始序列的ADF检验结果为：', ADF(train['on_man']))  # 检验训练集平稳性
print('白噪声检验结果为：', acorr_ljungbox(train['on_man'], lags=1))