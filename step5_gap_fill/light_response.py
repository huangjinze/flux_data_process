import numpy as np
import pandas as pd
from scipy import optimize
from scipy import stats
import matplotlib.pyplot as plt

class LightResponse:
    def func(self, x, p):
        '''
        co2_flux = a*b*PAR/(a*PAR+b)+c
        :param x: 自变量
        :param p: 参数
        :return: 函数计算结果
        '''
        a, b, c = p
        return a * b * x / (a * x + b) + c

    def funcR(self, y_value, x_value):
        '''
        co2_flux = a*b*PAR/(a*PAR+b)+c
        :param x: 自变量
        :param p: 参数
        :return: 函数计算结果
        '''
        return y_value+'~a * b * '+x_value+' / (a * '+x_value+' + b) + c'



    def lr_gap(self, win_data, a, b, c, var_index, x_value):
        '''
        :param a,b,c: 在该窗口内拟合出来的参数
        :param var_index: 该窗口内co2_flux为null的索引
        :return: 该窗口内补全的数据
        '''
        gap_value = win_data.loc[var_index, (x_value)].map(lambda x: self.func(x, [a, b, c]))
        return gap_value



    def light_response(self, data, condition, y_value, x_value, interval=1000):
        '''
        先要找到生长季开始的时间
        :param data: 总的数据集合
        :param condition: 数据的限制条件
        :param y_value: 待插补的数据因变量:co2_flux
        :param x_value: 待插补的数据自变量:PAR
        :param interval: 参考的时间间隔
        :return: 插补后的数据集合
        '''
        import rpy2.robjects as robjects
        from rpy2.robjects import r, pandas2ri
        from rpy2.robjects.packages import importr
        pandas2ri.activate()
        base = importr('base')
        stats = importr('stats')
        # 白天的数据重新设置索引
        # Day_data = data[condition].set_index([list(range(len(data[condition])))])
        Day_data = data[condition]

        temp_data = Day_data[['date_time', y_value, x_value]]


        temp_data_len = temp_data.index.tolist()
        for i in range(len(temp_data_len)):
            win_data = temp_data.iloc[i:i + interval]
            temp = win_data.dropna()
            mylist = r('list(a=-0.04, b=-10, c=2)')
            try:
                robjects.globalenv['df'] = temp
                A = stats.nls(
                    self.funcR(y_value, x_value),
                    start=mylist,
                    data=base.as_symbol('df')
                )

                pa = base.summary(A).rx2('coefficients')[9]
                pb = base.summary(A).rx2('coefficients')[10]
                pc = base.summary(A).rx2('coefficients')[11]
                if (pa < 0.05) and (pb < 0.05) and (pc < 0.05):
                    # print(data.ix[temp_data_len[i]]['date_time'])
                    # print(base.summary(A).rx2('coefficients'))
                    # life_time.append(data.ix[i]['date_time'])
                    a = base.summary(A).rx2('coefficients')[0]
                    b = base.summary(A).rx2('coefficients')[1]
                    c = base.summary(A).rx2('coefficients')[2]
                    # 筛选的条件:找出win_data中的co2_flux 的缺失值索引,并且时间在4-10月的
                    NANCondition = (win_data[y_value].isnull().values == True) & ()
                    # 该窗口内缺失值的索引
                    var_index = win_data[NANCondition].index.tolist()

                    gap_value = self.lr_gap(win_data, a, b, c, var_index, x_value)
                    temp_data.loc[var_index, (y_value)] = gap_value

            except:
                continue
        # print(life_time)
        # print(len(life_time))
        # data[condition, y_value] = temp_data[y_value]
        return data





if __name__ == '__main__':
    pass

