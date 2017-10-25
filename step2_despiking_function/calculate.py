import pandas as pd
import numpy as np

# % Calculate double differenced time series %
# data 是DataFrame的值
# return Series: co2_diff
def Calculate_Diff(data, value):
    a = data[value]
    b = a.shift(1)
    c = a.shift(-1)
    temp_value = (a-c)-(b-a)
    return temp_value

def Diff_test():
    import pandas as pd
    import numpy as np
    a = pd.DataFrame([1, 3, 5, 7, np.nan, 9, 11])
    print(a)
    b = a.shift(1)
    c = a.shift(-1)
    print(b)
    print(c)
    print((a - c) - (b - a))

# 计算Md的值
# data 是DataFrame的值
# return: pd.DataFrame : windowID, co2_Md
def Calculate_Md(data):
    Md_data = data.groupby(by=['windowID', 'daytime'], as_index=False).median()
    # data = Md_data.rename(columns={'co2_flux': 'Md_co2'})
    data = {
        'windowID': Md_data['windowID'],
        'daytime': Md_data['daytime'],
        'flux_Md': Md_data['diff_flux']
    }
    return pd.DataFrame(data)

def Calculate_Md_test():
    import pandas as pd
    import numpy as np
    a = pd.DataFrame({
        'windowID': [1, 1, 1, 2, 2, 2, 2],
        'co2_flux': [11, 11, 11, 12, 123, 41, 53],
        'num2': [-11, -11, -11, -102, -123, -401, -53]
    })
    Calculate_Md(a)

# 计算MAD的值
# return a number
def Calculate_MAD(data):

    # 执行abs(di-Md)
    MAD = (data['diff_flux'] - data['flux_Md']).abs().median()
    return MAD


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    z = 4
    a = pd.DataFrame({
        'windowID': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'co2_flux': [11, 24, 11, 2, 4, 65, 99, 123, 41, 53],
        'num2': [-11, -11, -11, -102, 65, 99, 123, -123, -401, -53],
        'daytime': [0, 0,  0, 1, 1, 1, 1, 0, 0, 0]
    })

    # print(a)
    window_nums = 1
    # 根据每个window的值计算对应的MAD和Md
    for i in range(1, window_nums+1):
        print('i:', i)
        # window i 白天的数据
        Day_Condition = (a['windowID'] == i) & (a['daytime'] == 1)
        Night_Condition = (a['windowID'] == i) & (a['daytime'] == 0)
        data_D = a[Day_Condition]
        data_N = a[Night_Condition]

        temp_diff = Calculate_Diff(data_D, 'co2_flux')
        a.loc[temp_diff.index, 'diff_flux'] = temp_diff

        temp_diff = Calculate_Diff(data_N, 'co2_flux')
        a.loc[temp_diff.index, 'diff_flux'] = temp_diff

        data_D = a[Day_Condition]
        data_N = a[Night_Condition]
        # 合并白天的数据：第一次计算的中位数Md
        Day = Calculate_Md(data_D)
        a.ix[data_D.index.tolist(), 'flux_Md'] = Day['flux_Md'].values[0]
        # 合并晚上的数据：第一次计算的中位数Md
        Night = Calculate_Md(data_N)
        a.ix[data_N.index.tolist(), 'flux_Md'] = Night['flux_Md'].values[0]
        # 计算MAD的数据
        data_D = a[Day_Condition]
        data_N = a[Night_Condition]
        a.ix[data_D.index.tolist(), 'flux_MAD'] = Calculate_MAD(data_D)
        a.ix[data_N.index.tolist(), 'flux_MAD'] = Calculate_MAD(data_N)

    print(a)
#
#     # data = pd.merge(
#     #     a, Md,
#     #     how='left', on='windowID')
#
#
#
#     # MAD = Calculate_MAD(data)
#     # print(data)
#     # print(MAD)
#     # threshold_1 = data['co2_Md'] - (z*MAD)/0.6745
#     # threshold_2 = data['co2_Md'] + (z*MAD)/0.6745
#     # print(threshold_1)
#     # print(threshold_2)
#     # condition = (data.co2_flux < threshold_1) | (data.co2_flux > threshold_2)
