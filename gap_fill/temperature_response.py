import numpy as np
from scipy import optimize
import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
from sklearn.metrics import r2_score

pandas2ri.activate()
base = importr('base')
stats = importr('stats')

class TemperatureResponse:
    def func(self, x, p):
        '''
        co2_flux = a*exp(T*b)
        :param x: 自变量 T:土壤表层或气温，R^2高用哪个
        :param p: 参数
        :return: 函数计算结果
        '''
        a, b = p
        return a * np.exp(x*b)

    def funcR(self, y_value, x_value):
        '''
        co2_flux = a*exp(Ta*b)
        :param x: 自变量
        :param p: 参数
        :return: 函数计算结果
        '''
        return y_value+'~a * exp( '+x_value+'* b)'



    def tr_gap(self, data, p, var_index, x_value):
        '''
        :param p: 在该窗口内拟合出来的参数
        :param var_index: 该窗口内co2_flux为null的索引
        :return: 该窗口内补全的数据
        '''
        gap_value = data.loc[var_index, (x_value)].map(lambda x: self.func(x, p))
        return gap_value

    def air_temperature_response(self, data, condition, y_value, x_value):
        '''
        先要找到生长季开始的时间
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

    def soil_temperature_response(self, data, condition, y_value, x_value):
        '''
        先要找到生长季开始的时间
        :param data: 总的数据集合
        :param condition: 数据的限制条件
        :param y_value: 待插补的数据因变量:co2_flux
        :param x_value: 待插补的数据自变量:土壤表层 temperature
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

    def temperature_response(self, data, condition, y_value, x_value, var_index):
        '''
        先要找到生长季开始的时间
        :param data: 总的数据集合
        :param condition: 数据的限制条件
        :param y_value: 待插补的数据因变量:co2_flux
        :param x_value: 待插补的数据自变量名称:air temperature
        :return: 插补后的数据集合
        '''
        soilP, soilRsq = self.soil_temperature_response(data, condition, y_value, x_value[0])
        airP, airRsq = self.air_temperature_response(data, condition, y_value, x_value[1])

        # NANCondition = (data[y_value].isnull().values == True)
        # var_index = data[NANCondition].index.tolist()

        if airRsq < soilRsq:
            gap_value = self.tr_gap(data, soilP, var_index, x_value[0])
        else:
            gap_value = self.tr_gap(data, airP, var_index, x_value[1])
        print(gap_value)
        data.loc[var_index, (y_value)] = gap_value
        return data
