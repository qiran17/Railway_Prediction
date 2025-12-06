import numpy as np
import pandas as pd
import re


def Deal_Fun(n_file, filedata, SaveFile_Name):
    for m in range(n_file):
        # `.xlsx`、`.xls`、`.xlsm` 等 Excel 文件pd.read_excel()
        # `.csv`pd.read_csv()
        data = pd.read_excel(filedata[m])
        row = data.shape[0]  # row为data的总行数
        Head_d = []  # 始发日期
        Line = []  # 列车名字
        for i in range(row):
            if '始发日期' in data.iloc[i, 0]:
                Head_d.append(re.findall('[0-9\—]+', data.iloc[i, 0]))
            if data.iloc[i, 0] == '上车站':
                Line.append(re.findall('[A-Z]{2}[0-9]{2} ', data.iloc[i - 1, 0]))
        Line = pd.DataFrame(Line)  # 以数据框形式存放上车站
        Head_d = pd.DataFrame(Head_d)
        # 新加'Head'列(Line.iloc[i,1];)，并将Head_d[0, 0]赋值给 Line['Head']
        Line['Head'] = 0
        for i in range(len(Line)):
            Line.iloc[i, 1] = Head_d.iloc[0, 0]

        on_station = []  # on_station = [i for i, x in enumerate(data.iloc[:, 0]) if x == '上车站']
        on_count = []
        for i, x in enumerate(data.iloc[:, 0]):
            if x == '上车站':
                on_station.append(i)
        for i, x in enumerate(data.iloc[:, 0]):
            if x == '上车人数合计':
                on_count.append(i)
        Size = pd.DataFrame(np.zeros([len(on_station), 2]), columns=['on_station', 'on_count'])
        Size['on_station'] = on_station
        Size['on_count'] = on_count
        Size['off_count'] = 0
        for h in range(len(Size.iloc[:, 0])):
            Size.loc[h, 'off_count'] = [i for i, x in enumerate(data.iloc[Size.iloc[h, 0], :]) if x == '下车人数合计'][0]

        # guodu为文件中第一列的数据
        guodu = pd.DataFrame(data.iloc[:, 0])
        off_station = []
        for j in range(len(Size.iloc[:, 0])):
            off_station.append(guodu.iloc[Size.iloc[j, 0] + 2:Size.loc[j, 'on_count'], 0])
        sum_station = 0
        for i in range(len(off_station)):
            sum_station = sum_station + len(off_station[i])
        Out_off = pd.DataFrame(np.zeros([sum_station, 3]),columns=['off_station', 'off_man', 'off_time'])
        h = 0
        for i in range(len(off_station)):
            Out_off.iloc[h:h + len(off_station[i]), 0] = list(off_station[i])
            h = h + len(off_station[i])
        off_man = []
        for i in range(len(Size)):
            # data1为文件中'下车人数合计'那一列的数据
            data1 = pd.DataFrame(data.iloc[:, Size.loc[i, 'off_count']])
            off_man.append(data1.iloc[Size.iloc[i, 0] + 2:Size.loc[i, 'on_count'], 0])
        h = 0
        for i in range(len(off_man)):
            Out_off.iloc[h:h + len(off_man[i]), 1] = list(off_man[i])
            h = h + len(off_man[i])
        off_time = []
        for i in range(len(Size)):
            # data1为文件中第二列的数据
            data1 = pd.DataFrame(data.iloc[:, 1])
            off_time.append(data1.iloc[Size.iloc[i, 0] + 2:Size.loc[i, 'on_count'], 0])
        h = 0
        for i in range(len(off_time)):
            Out_off.iloc[h:h + len(off_time[i]), 2] = list(off_time[i])
            h = h + len(off_time[i])

        Come = pd.DataFrame(np.zeros([sum_station, 3]), columns=['on_station', 'on_man', 'on_time'])
        on_station1 = []
        for i in range(len(Size)):
            data1 = pd.DataFrame(data.iloc[Size.loc[i, 'on_station'], :])
            on_station1.append(data1.iloc[2:Size.loc[i, 'off_count'], 0])
        h = 0
        for i in range(len(on_station1)):
            Come.iloc[h:h + len(on_station1[i]), 0] = list(on_station1[i])
            h = h + len(on_station1[i])
        # 上车人数
        on_man = []
        for i in range(len(Size)):
            data1 = pd.DataFrame(data.iloc[Size.loc[i, 'on_count'], :])
            on_man.append(data1.iloc[2:Size.loc[i, 'off_count'], 0])
        h = 0
        for i in range(len(on_man)):
            Come.iloc[h:h + len(on_man[i]), 1] = list(on_man[i])
            h = h + len(on_man[i])
        # 上车时间
        on_time = []
        for i in range(len(Size)):
            data1 = pd.DataFrame(data.iloc[Size.loc[i, 'on_station'] + 1, :])
            on_time.append(data1.iloc[2:Size.loc[i, 'off_count'], 0])
        h = 0
        for i in range(len(on_time)):
            Come.iloc[h:h + len(on_time[i]), 2] = list(on_time[i])
            h = h + len(on_time[i])

        # 创建Station数据框架统合
        Station = pd.DataFrame(np.zeros([len(Out_off), 7]), columns=['on_station', 'on_man', 'on_time',
                                                                     'off_man', 'off_time', 'date', 'train'])
        # 注：因为下车站点要始终多上车站点1个，所以方便统计使用下车站点作为站点信息存储
        Station['on_station'] = list(Out_off.iloc[:, 0])
        Station['off_man'] = list(Out_off['off_man'])
        Station['off_time'] = list(Out_off['off_time'])
        k = 0
        # 以off_man[i] off_station[i] off_time[i]中任意一个作为循环数据组尺度
        for i in range(len(on_man)):
            Station.loc[k:k + len(on_man[i]) - 1, 'on_man'] = list(on_man[i])
            Station.loc[k:k + len(on_time[i]) - 1, 'on_time'] = list(on_time[i])
            # 缺省值填充
            Station.loc[k + len(on_time[i]):k - 1 + len(off_time[i]), 'on_time'] = 0.1
            Station.loc[k + len(on_man[i]):k - 1 + len(off_man[i]), 'on_man'] = 0.1
            # 补充日期与车次信息
            Station.loc[k:k - 1 + len(off_man[i]), 'date'] = Line.iloc[i, 1]
            Station.loc[k:k - 1 + len(off_man[i]), 'train'] = Line.iloc[i, 0]
            k = k + len(off_man[i])

        Station.to_csv(SaveFile_Name, encoding="utf-8", index=False, header=False, mode='a+')
