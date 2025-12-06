import pandas as pd
import matplotlib.pyplot as plt

Train_Station = pd.read_csv('./tmp/Train_Station.csv', index_col=0, encoding='utf-8')
on = pd.DataFrame(Train_Station['on_station'])
on = on.drop_duplicates()  # 剔除重复名字
on['on_mean'] = 0
on['off_mean'] = 0
for i in range(len(on)):
    data = Train_Station[Train_Station.iloc[:, 0] == on.iloc[i, 0]]
    on.iloc[i, 1] = sum(data.iloc[:, 1]) / (len(data))
    on.iloc[i, 2] = sum(data.iloc[:, 3]) / (len(data))
on_sample = on.sample(20, random_state=44)
on_sample.index = on_sample['on_station']
plt.xticks(rotation=45)
on_sample.plot(kind='bar', title='analysis of people')
plt.ylabel('on and off mans')
plt.xlabel('stations')
plt.show()