import step2_despiking_function.calculate as Calculation
import numpy as np
# 计算Md的值
def Md_Method(data_D, data_N, data):
    # 合并白天的数据：第一次计算的中位数Md
    Day = Calculation.Calculate_Md(data_D)
    try:
        a = Day['flux_Md'].values[0]
    except:
        a = np.nan
    data.ix[data_D.index.tolist(), 'flux_Md'] = a

    # 合并晚上的数据：第一次计算的中位数Md
    Night = Calculation.Calculate_Md(data_N)
    try:
        a = Night['flux_Md'].values[0]
    except:
        a = np.nan
    data.ix[data_N.index.tolist(), 'flux_Md'] = a

    return data

def MAD_Method(data_D, data_N, data):
    try:
        a = Calculation.Calculate_MAD(data_D)
    except:
        a = np.nan
    data.ix[data_D.index.tolist(), 'flux_MAD'] = a
    try:
        a = Calculation.Calculate_MAD(data_N)
    except:
        a = np.nan
    data.ix[data_N.index.tolist(), 'flux_MAD'] = a

    return data