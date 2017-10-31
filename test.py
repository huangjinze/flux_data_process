
#-*-coding:utf-8-*-

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import stats
from scipy import optimize

def func(PAR, p):
    '''
    co2_flux = a*b*PAR/(a*PAR+b)+c
    :param x: 閼奉亜褰夐柌锟�
    :param p: 閸欏倹鏆�?
    :return: 閸戣姤鏆熺拋锛勭暬缂佹挻鐏�
    '''
    a, b, c = p
    return a*b*PAR/(a*PAR+b)+c
    # return a*PAR+b+c
    # return PAR*a*b+c

def residuals(p, y, x):
    '''
    鐎圭偤鐛欓弫鐗堝祦x, y 閸滃本�?�欓崥鍫濆毐閺侀绠ｉ梻瀵告畱�?�割噯绱漰娑撴椽娓剁憰浣瑰閸掓壆娈戠化缁樻�?
    :param p:
    :param y:
    :param x:
    :return:
    '''
    return np.square(y - func(x, p))

def scipytest():
    import numpy as np
    import statsmodels.api as sm
    nsample = 100
    x = np.linspace(0, 10, nsample)
    X = sm.add_constant(x)

    a = 1
    b = 3
    c = 5
    e = np.random.normal(size=nsample)
    y = a*b*x/(a*x+b)+c

    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())

def linearTest():
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [6.1, 11.2, 16.5, 21.1, 26.2, 31.5, 35.6, 40.9, 46.3, 51.02]
    # y = [1, 16, 81, 256, 625, 1296, 2401, 4096, 6561, 1000]
    # y = [6, 11, 16, 21, 26, 31, 36, 41, 46, 51]
    y = pd.Series(y)
    x = pd.Series(x)

    p0 = [7, 0.4, 1]
    plsq = optimize.leastsq(residuals, p0, args=(y, x))
    ym = func(x, plsq[0])
    print()
    print(u'閸欏倹鏆熼敍锟�', plsq[0])
    print(u'閼奉亜褰夐柌寮�:', x)
    print(u'閹风喎鎮庣紒鎾寸�?:', ym)
    print('ttest_ind:', stats.ttest_ind(x, ym, equal_var=True))
    print('levene', stats.levene(x, ym))
    print('ttest_1samp', stats.ttest_1samp(ym, np.mean(y)))
    print(func(1000, plsq[0]))
    print(ym.describe())

def draw_fill():
    dataset = pd.read_excel(
        'data/yc_1_2012_QAQC.xlsx',
                header=0,
                usecols=['CO2_filled_nlm'],
                skiprows=[1]
            )

    plt.figure(figsize=(16, 4))
    plt.scatter(range(dataset.shape[0]), dataset['CO2_filled_nlm'], label='Gap_Fill',color='r')

    plt.legend()
    plt.show()


def func(x, p):
    '''
    co2_flux = a*b*PAR/(a*PAR+b)+c
    :param x: 自变量
    :param p: 参数
    :return: 函数计算结果
    '''
    a, b, c = p
    return a * b * x / (a * x + b) + c

def dicttest():
    df = pd.DataFrame({'animal': 'cat dog cat fish dog cat cat'.split(),
                       'size': list('SSMMMLL'),
                       'weight': [8, np.nan, 11, 1, np.nan, 12, 12],
                       'adult': [False] * 5 + [True] * 2},
                      index=[10, 20,30,40,50,60,70])
    print(df)
    i = 1
    a = df[df['weight'].index >= 50]
    b = a[['size', 'weight']]
    print(a)
    print(b)
    b.loc[50, 'weight'] = 1
    print(b.index.tolist())
    # p = df.loc[[30, 50], 'weight']
    p = b.loc[[60, 70], 'weight'].map(lambda x: func(x, [1,2,3]))
    print(p)
    df.loc[b.index.tolist(), ('weight')] = b['weight']
    print(df)

def usesm():
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    import patsy

    # nobs = 100
    # X = np.random.random((nobs, 2))
    # X = sm.add_constant(X)
    # beta = [1, .1, .5]
    # e = np.random.random(nobs)
    # y = np.dot(X, beta) + e
    # results = sm.OLS(y, X).fit()
    # print(results.summary())

    dat = pd.read_csv('data/Guerry.csv')
    vars = ['Department', 'Lottery', 'Literacy', 'Wealth']
    df = dat[vars]
    df['a'] = 1
    df['b'] = 1
    print(df.tail())
    a = 1
    b = 1
    f = 'Lottery~a*Literacy+Wealth/b'
    y, X = patsy.highlevel.dmatrices(func, data=df, return_type='dataframe')
    mod = sm.OLS(y, X)
    res = mod.fit()
    print(res.summary())



if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    # scipytest()
    # linearTest()
    # draw_fill()
    dicttest()
    # usesm()
    # Rtest()
    # PAR()


