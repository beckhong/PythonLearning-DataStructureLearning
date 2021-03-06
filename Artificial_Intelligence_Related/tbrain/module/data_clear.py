import matplotlib.pyplot as plt
from tbrain.module.import_tfbrain_data import read_tbrain_data

startTime = '20180408'
endTime = '20180605'
codeNum = 1101

def showDataTrend(x,y):
    plt.figure()
    plt.plot(x,y)
    plt.show()

# for a better version should use [array] - [0,array[:len(array)-1]
def calculate_amplitude(data_price):
    diff_values = []
    amplitude_signs = []

    for i in range(len(data_price)):
        if i == 0:
            amplitude_signs.append(0)
            diff_values.append(0)
        else:
            diff_value = data_price[i] - data_price[i-1]
            diff_values.append(diff_value)
            if diff_value < 0:
                amplitude_signs.append(0)
            else:
                amplitude_signs.append(1)

    return amplitude_signs, diff_values

# Df = read_tbrain_data('../data/taetfp.csv')
# [  50   51   52   53   54   55   56   57   58   59 6201 6203 6204 6208
#   690  692  701  713]
# 18
# Df = read_tbrain_data('../data/tasharep.csv')
# Df = read_tbrain_data('../data/tetfp.csv')
# [  50   51   52   53   54   55   56   57   58   59 6201 6203 6204 6208
#   690  692  701  713]
# 18
Df = read_tbrain_data('../data/tsharep.csv')

# print(Df.info())
unique_code = Df.code.unique()
print(unique_code)
print(len(unique_code))


trainDf = Df[(Df.code == codeNum)]

# print(trainDf.head())
trainDf.index= trainDf.date

trainDf.to_csv('test.csv', sep='\t')

"""
# 使用最近一兩年的資料
trainDf.index = trainDf.date
trainDF = trainDf[startTime:endTime]

# 找尋是否有趨勢
# showDataTrend(trainDF.date,trainDF.open)

# sample data if needed
# data = data[-20:]
data_amp, data_diff_values = calculate_amplitude(trainDF.open)
print(data_amp)
print('data length %d'%len(trainDf.date))
plt.plot(trainDF.date, data_diff_values,'ro')
plt.show()
"""