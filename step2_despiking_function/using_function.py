import step2_despiking_function.calculate as Calculation
import numpy as np

# 判断白天黑夜的值
def judge_d_n(ctype, data, threshold):
    import step2_despiking_function.judge_d_n as judge_DN
    judge_dn = {}
    judge_dn['par'] = judge_DN.DNContext(judge_DN.PAR())
    judge_dn['slr'] = judge_DN.DNContext(judge_DN.SLR())

    if ctype in judge_dn.keys():
        cc = judge_dn[ctype]
    else:
        print("Undefine type. Use PAR mode.")
        cc = judge_dn['par']
    return cc.get_method(data, threshold)

# % Calculate double differenced time series %
# data 是DataFrame的值
# return Series: co2_diff
def Calculate_Diff(data, value):
    a = data[value]
    b = a.shift(1)
    c = a.shift(-1)
    temp_value = (a-c)-(b-a)
    return temp_value

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