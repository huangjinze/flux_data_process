import pandas as pd
import numpy as np

def calculate_Md(data, value):
    '''
    calculate Md value
    :param data: <dataframe> data set including co2_Md
    :param value: index need to calculate
    :return: <dataframe> =windowID=,=daytime=,={value}_Md=
    '''
    Md_data = data.groupby(by=['windowID', 'daytime'], as_index=False).median()
    data = {
        'windowID': Md_data['windowID'],
        'daytime': Md_data['daytime'],
        value+'_Md': Md_data[value+'_diff']
    }
    return pd.DataFrame(data)


def calculate_MAD(data, value):
    '''
    calculate MAD value
    :param data: <dataframe> data set including {value}_Md
    :param value: <value> index need to calculate MAD
    :return: <float>{value}_MAD
    '''

    MAD = (data[value+'_diff'] - data[value+'_Md']).abs().median()
    return MAD



if __name__ == '__main__':
    # import pandas as pd
    # import numpy as np
    #
    # s1 = np.array([1, 2, 3, np.nan])
    # s2 = np.array([5, np.nan, np.nan, np.nan])
    # df = pd.DataFrame([s1, s2])
    # print(df)
    # df['Col_sum'] = df.apply(lambda x: x.mean(), axis=1)
    # print(df)
    # 从数据库中读取数据
    pass