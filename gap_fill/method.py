import despiking_function.power_close_analysis as PCA
import gap_fill.MDT as MDT
import gap_fill.light_response as LR
import gap_fill.linear_insert as LI
import gap_fill.temperature_response as TR
import gap_fill.linear_relation as LRL

class Facade:
    def __init__(self):
        self.linear_insert = LI.LinearInsert()
        self.mdt = MDT.MDT()
        self.lr = LR.LightResponse()
        self.tr = TR.TemperatureResponse()
        self.lrl = LRL.LinearRelation()
    def MethodA(self, data, value, li_interval=4, mdt_interval=384):
        '''
        MDT
        :param data: gap data
        :param value: value need to be filled
        :param condition: day or night
        :return: filled data
        '''
        print("linear insert + mdt:")
        # #白天的条件
        Day_Condition = (data['daytime'] == 1)
        # 夜晚的筛选条件
        Night_Condition = (data['daytime'] == 0)

        data = self.linear_insert.linear_insert_method(data, value, li_interval)
        # MDT 方法补全
        # 白天的筛选条件
        data = self.mdt.mdt_method(data, Day_Condition, value, mdt_interval)
        # 夜晚的筛选条件
        data = self.mdt.mdt_method(data, Night_Condition, value, mdt_interval)
        return data


    def MethodB(self, data, value, x_lr_value, x_tr_value, li_interval=4):
        '''
        linear insert+light response+temperature response
        :param data:
        :param value:<string> 'co2_flux'
        :param x_lr_value:<string> 'PAR'
        :param x_tr_value:<list>(Soil T and AIR T)
        :param li_interval:
        :return:
        '''
        print("linear insert + light response:")
        data = self.linear_insert.linear_insert_method(data, value, li_interval)
        # #白天的条件
        Day_Condition = (data['daytime'] == 1)

        #光反应插补之前的缺失索引
        NANCondition = (data[value].isnull().values == True) & Day_Condition
        var_index_before_lr = data[NANCondition].index.tolist()
        data, growing_time_index = self.lr.light_response(data, Day_Condition, value, x_lr_value)
        # data.to_csv('lr.csv')
        # 光反应插补之后的缺失索引
        # NANCondition = (data[value].isnull().values == True) & Day_Condition
        # print(data[NANCondition].index.tolist())
        # print(len(data[NANCondition].index.tolist()))

        # 夜晚的筛选条件
        #非生长季白天和夜晚的缺失值索引应该为 var_index_before_lr - growing_time_index

        var_index_night = list(set(var_index_before_lr)^set(growing_time_index))
        Night_Condition = (data['daytime'] == 0)
        data = self.tr.temperature_response(data, Night_Condition, value, x_tr_value, var_index_night)
        return data
    #     self.three.MethodThree()

    # def MethodC(self, data, value, x_lr_value, x_tr_value, li_interval=4):

    def MethodC(self, data, x_value, y_value):


if __name__ == '__main__':
    import pandas as pd

    value = 'co2_flux'
    data = pd.read_csv('lr.csv')
    NANCondition = (data[value].isnull().values == True)
    Night_Condition = (data['daytime'] == '0')
    x_tr_value = ['soil_T_1_10cm_Avg', 'Ta_Avg']
    var_index_night = data[NANCondition].index.tolist()

    a = Facade()
    data = a.tr.temperature_response(data, Night_Condition, value, x_tr_value, var_index_night)

