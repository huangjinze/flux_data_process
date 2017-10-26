import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import stats
from scipy import optimize
import statsmodels.api as sm

def func(PAR, p):
    '''
    co2_flux = a*b*PAR/(a*PAR+b)+c
    :param x: 自变量
    :param p: 参数
    :return: 函数计算结果
    '''
    a, b, c = p
    # return a*b*PAR/(a*PAR+b)+c
    return a*PAR+b+c
    # return PAR*a*b+c

def residuals(p, y, x):
    '''
    实验数据x, y 和拟合函数之间的差，p为需要找到的系数
    :param p:
    :param y:
    :param x:
    :return:
    '''
    return y - func(x, p)

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # y = [6.1, 11.2, 16.5, 21.1, 26.2, 31.5, 35.6, 40.9, 46.3, 51.02]
    y = [1, 16, 81, 256, 625, 1296, 2401, 4096, 6561, 1000]
    # y = [6, 11, 16, 21, 26, 31, 36, 41, 46, 51]
    y = pd.Series(y)
    x = pd.Series(x)

    p0 = [7, 0.4, 1]
    plsq = optimize.leastsq(residuals, p0, args=(y, x))
    ym = func(x, plsq[0])
    print('参数：', plsq[0])
    print('自变量x:', x)
    print('拟合结果:', ym)
    print('ttest_ind:', stats.ttest_ind(x, ym, equal_var=True))
    print('levene', stats.levene(x, ym))
    print('ttest_1samp', stats.ttest_1samp(ym, np.mean(y)))
    print(func(1000, plsq[0]))

    # dataset = pd.read_excel(
    #     'data/yc_1_2012_QAQC.xlsx',
    #             header=0,
    #             usecols=['CO2_filled_nlm'],
    #             skiprows=[1]
    #         )
    #
    # plt.figure(figsize=(16, 4))
    # plt.scatter(range(dataset.shape[0]), dataset['CO2_filled_nlm'], label='Gap_Fill',color='r')
    #
    # plt.legend()
    # plt.show()

