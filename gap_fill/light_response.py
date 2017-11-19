import numpy as np
import pandas as pd
from scipy import optimize
from scipy import stats
import matplotlib.pyplot as plt

class LightResponse:
    def func(self, x, p):
        '''
        co2_flux = a*b*PAR/(a*PAR+b)+c
        :param x: x
        :param p: parameter
        :return: y
        '''
        a, b, c = p
        return a * b * x / (a * x + b) + c

    def funcR(self, y_value, x_value):
        '''
        co2_flux = a*b*PAR/(a*PAR+b)+c
        :param x: x
        :param p: parameter
        :return: y
        '''
        return y_value+'~a * b * '+x_value+' / (a * '+x_value+' + b) + c'



    def lr_gap(self, win_data, a, b, c, var_index, x_value):
        '''
        :param a,b,c: the parameter in the i_th_window
        :param var_index: in special window, the index of value value is null
        :return: in special window, the gap-filled value
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
        :return: 插补后的数据集合,生长季的索引
        '''
        import rpy2.robjects as robjects
        from rpy2.robjects import r, pandas2ri
        from rpy2.robjects.packages import importr
        pandas2ri.activate()
        base = importr('base')
        stats = importr('stats')

        Day_data = data[condition]

        temp_data = Day_data[['date_time', y_value, x_value]]
        growing_time = []
        data_index = temp_data.index.tolist()
        # year = Day_data.loc[var_index[0]]['date_time'].year

        for i in range(len(data_index)-interval):
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
                    # print(data.ix[var_index[i]]['date_time'])
                    # print(base.summary(A).rx2('coefficients'))
                    a = base.summary(A).rx2('coefficients')[0]
                    b = base.summary(A).rx2('coefficients')[1]
                    c = base.summary(A).rx2('coefficients')[2]
                    # 筛选的条件:找出win_data中的co2_flux 的缺失值索引,并且时间在4-10月的
                    # timeCondition = ((win_data['date_time'] > year+'-04') &
                    #      (win_data['date_time'] < year+'-10'))
                    NANCondition = (win_data[y_value].isnull().values == True)
                    # print(data.ix[data_index[i]]['date_time'].month)
                    if data.ix[data_index[i]]['date_time'].month>=4 and  data.ix[data_index[i]]['date_time'].month<=11:
                        growing_time.append(data_index[i])
                        # print(data.ix[data_index[i]]['date_time'])
                        # 该窗口内缺失值的索引
                        win_var_index = win_data[NANCondition].index.tolist()

                        gap_value = self.lr_gap(win_data, a, b, c, win_var_index, x_value)
                        temp_data.loc[win_var_index, (y_value)] = gap_value

            except:
                continue

        data.loc[data_index, y_value] = temp_data[y_value]
        return data, growing_time





if __name__ == '__main__':
    pass

