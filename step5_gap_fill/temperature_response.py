import numpy as np
from scipy import optimize

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
        # temp_data = data[condition].set_index([list(range(len(data[condition])))])
        Day_data = data[condition]
        # print(temp_data)

        temp_data = Day_data[['date_time', y_value, x_value]]

        for i in temp_data.index.tolist():
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
                    a = base.summary(A).rx2('coefficients')[0]
                    b = base.summary(A).rx2('coefficients')[1]
                    c = base.summary(A).rx2('coefficients')[2]
                    # 筛选的条件:找出win_data中的co2_flux 的缺失值索引
                    NANCondition = (win_data[y_value].isnull().values == True)
                    # 该窗口内缺失值的索引
                    var_index = win_data[NANCondition].index.tolist()

                    gap_value = self.lr_gap(win_data, a, b, c, var_index, x_value)
                    temp_data.loc[var_index, (y_value)] = gap_value
                    print('**************************')
                    print(gap_value)
                    print(temp_data.loc[var_index, y_value])
                    print('**************************')
            except:
                continue
        data[Condition, y_value] = temp_data[y_value]
        return data
if __name__ == '__main__':
    # def func(x, p):
    #     A, k, theta = p
    #     return A*np.sin(2*np.pi*k*x+theta)
    # def residuals(p, y, x):
    #     return y-func(x, p)
    #
    # x=np.linspace(0, 2*np.pi, 100)
    # A, k, theta = 10, 0.34, np.pi/6
    # y0 = func(x, [A, k, theta])
    # np.random.seed(0)
    # y1 = y0+2*np.random.randn(len(x))
    #
    # p0 = [7, 0.40, 0]
    #
    # plsq = optimize.leastsq(residuals, p0, args=(y1, x))
    # plsq1 = np.linalg.lstsq(y1, x)
    #
    # print([A, k, theta])
    # print(plsq)
    # print(plsq1)

    import matplotlib.pyplot as plt
    from scipy import stats
    x = np.linspace(-5, 5, 500)
    print(np.mean(x))
    print(np.var(x))
    print(stats.ttest_1samp(x, 1))