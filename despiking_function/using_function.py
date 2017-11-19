import despiking_function.calculate as Calculation
import numpy as np
import despiking_function.power_close_analysis as PCA

def judge_d_n(ctype, data, threshold):
    '''
    judge day or night
    :param ctype: <string> judge method: par or slr
    :param data: <dataframe> original data including =daytime=
    :param threshold: <int> day and night threshold, if par: 5
    :return:<dataframe> change =daytime= 'T/F' to '1/0'
    '''
    import despiking_function.judge_d_n as judge_DN
    judge_dn = {}
    judge_dn['par'] = judge_DN.DNContext(judge_DN.PAR())
    judge_dn['slr'] = judge_DN.DNContext(judge_DN.SLR())

    if ctype in judge_dn.keys():
        cc = judge_dn[ctype]
    else:
        print("Undefine type. Use PAR mode.")
        cc = judge_dn['par']
    return cc.get_method(data, threshold)


def calculate_Diff(data, value):
    '''
    Calculate double differenced time series
    :param data: <dataframe> data including =diff=
    :param value: <string> index need to be difference
    :return: <Series> co2_diff
    '''
    a = data[value]
    b = a.shift(1)
    c = a.shift(-1)
    temp_value = (a-c)-(b-a)
    return temp_value


def md_Method(data_D, data_N, data, value):
    '''
    # calculate MD
    :param data_D:  <dataframe>day data
    :param data_N:  <dataframe>night data
    :param data: <dataframe>data set
    :param value: <string> index need to calculate md
    :return:  <dataframe> data set including {value}_md
    '''
    # day's data_md
    Day = Calculation.calculate_Md(data_D, value)
    try:
        a = Day[value+'_Md'].values[0]
    except:
        a = np.nan
    data.ix[data_D.index.tolist(), value+'_Md'] = a

    # night's data_md
    Night = Calculation.calculate_Md(data_N, value)
    try:
        a = Night[value+'_Md'].values[0]
    except:
        a = np.nan
    data.ix[data_N.index.tolist(), value+'_Md'] = a

    return data

def MAD_Method(data_D, data_N, data, value):
    '''
        # calculate MD
    :param data_D:  <dataframe>day data
    :param data_N:  <dataframe>night data
    :param data: <dataframe>data set
    :param value: <string> index need to calculate mad
    :return:  <dataframe> data set including {value}_mad
    '''
    try:
        a = Calculation.calculate_MAD(data_D, value)
    except:
        a = np.nan
    data.ix[data_D.index.tolist(), value+'_MAD'] = a
    try:
        a = Calculation.calculate_MAD(data_N, value)
    except:
        a = np.nan
    data.ix[data_N.index.tolist(), value+'_MAD'] = a

    return data

def calculate_ET(data, Pw=1, alambda=2.45):
    '''
    if calculate power and water
    :param data: <dataframe>data including =LE=
    :param Pw: <float>water's density, default 1
    :param alambda: <float>water Hg，default 2.45
    :return: <dataframe>data,new data set
    '''
    if 'LE' in data.columns.tolist():
        data['ET'] = data['LE'] / (Pw * alambda)
    return data


def calculate_G(data):
    '''
    calculate G's mean value
    :param data: <dataframe>data set including =LE=,=H=,=Rn_Avg=,=G=
    :return: G
    '''
    soil_G = data[['soilG_1_Avg', 'soilG_2_Avg', 'soilG_3_Avg', 'soilG_4_Avg', 'soilG_5_Avg']]
    data['G_mean'] = soil_G.apply(lambda x: x.mean(), axis=1)
    return data

def calculate_PCA(data):
    '''
    calculate gradient of power close analysis
    :param data: <dataframe>data set including =LE=,=H=,=Rn_Avg=,=G=
    :return:
    '''
    if ('LE' in data.columns.tolist()) \
            and ('H' in data.columns.tolist()) \
            and ('Rn_Avg' in data.columns.tolist()) \
            and ('G' in data.columns.tolist()):
        PCA.PCA_method(data)
    return data