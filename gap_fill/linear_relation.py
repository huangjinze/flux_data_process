import numpy as np
from scipy import optimize
import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
from sklearn.metrics import r2_score

pandas2ri.activate()
base = importr('base')
stats = importr('stats')

class LinearRelation:
    def func(self, x, p):
        '''
        y = a*x+b
        :param x: 自变量
        :param p: 参数
        :return: 函数计算结果
        '''
        a, b = p
        return a * x + b

    def funcR(self, y_value, x_value):
        '''
         y = a*x+b
        :param x: 自变量
        :param p: 参数
        :return: 函数计算结果
        '''
        return y_value+'~a * '+x_value+'+ b)'

    def tr_gap(self, data, p, var_index, x_value):
        '''
        :param p: 拟合出来的参数
        :param var_index: 该窗口内y为null的索引
        :return: 补全的数据
        '''
        gap_value = data.loc[var_index, (x_value)].map(lambda x: self.func(x, p))
        return gap_value

    def linear_relation(self, data, condition, y_value, x_value):
        '''
        :param data: 总的数据集合
        :param condition: 数据的限制条件
        :param y_value: 待插补的数据因变量:co2_flux
        :param x_value: 待插补的数据自变量:air temperature
        :return: 插补后的数据集合
        '''

        # 夜晚的数据
        Night_data = data[condition]

        temp_data = Night_data[['date_time', y_value, x_value]]
        temp = temp_data.dropna()
        mylist = r('list(a=10, b=--0.04)')


        robjects.globalenv['df'] = temp
        A = stats.nls(
            self.funcR(y_value, x_value),
            start=mylist,
            data=base.as_symbol('df')
        )
        a = base.summary(A).rx2('coefficients')[0]
        b = base.summary(A).rx2('coefficients')[1]
        Rsq = r2_score(temp[y_value], self.func(temp[x_value], [a, b]))

        return [a, b], Rsq