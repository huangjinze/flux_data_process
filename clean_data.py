import pandas as pd
import filter_data
from datetime import datetime
import matplotlib.pyplot as plt
import opt_data
import db_operation.database as dbopt


class CleanData(object):
    def __init__(
            self, flux_data,
            met_data, file_name,
            value='co2_flux',
            day_size=13, z=4
    ):
        self.file_name = file_name
        self.z = z
        self.value = value

        # 以时间为主键，合并两个数据集合
        self.data = pd.merge(
            flux_data, met_data,
            how='right', left_on='date_time', right_on='TIMESTAMP')

        # 添加一列,window标签序号,如果最后一个的个数不够window_size的，则算前一个window
        window_size = day_size*48
        self.window_nums = self.data.shape[0] // window_size
        self.data['windowID'] = self.data.index // window_size
        if self.data.shape[0] % window_size != 0:
            condition = (self.data.windowID == self.window_nums)
            self.data.loc[condition, 'windowID'] = self.window_nums - 1


    # 第一步:check range，检查范围，因站点和变量而异
    def check_range(self, flux_down_range=-20.0, flux_up_range=20.0,):
        # 如果是盐池一号

        if self.file_name.find('yc_1_flux') >= 0:
            condition = (self.data[self.value] < flux_down_range) | (self.data[self.value] > flux_up_range)
            self.data = filter_data.set_data_nan(self.data, condition, self.value)

    # 第二步:despiking，根据气象数据剔除尖峰数据
    def despiking(self):
        import step2_despiking_function.judge_d_n as judge_DN
        import step2_despiking_function.calculate as Calculation
        import step2_despiking_function.using_function as Method
        # 进行白天黑夜判断，采用PAR的方法
        self.data = judge_DN.judge_DN_PAR(self.data)

        # print('despiking1:')
        # print(self.data)
        # 根据每个window的值计算对应的MAD和Md
        for i in range(0, self.window_nums):
        # for i in range(0, 1):
            # window i 白天的数据
            Day_Win_Condition = (self.data['windowID'] == i) & (self.data['daytime'] == 1)
            Night_Win_Condition = (self.data['windowID'] == i) & (self.data['daytime'] == 0)
            data_D = self.data[Day_Win_Condition]
            data_N = self.data[Night_Win_Condition]

            # print(data_D)
            # 对白天CO2_flux进行通量差分计算
            temp_diff = Calculation.Calculate_Diff(data_D, self.value)
            self.data.loc[temp_diff.index, 'diff_flux'] = temp_diff
            # print(self.data)

            # # 对夜晚CO2_flux进行通量差分计算
            temp_diff = Calculation.Calculate_Diff(data_N, self.value)
            self.data.loc[temp_diff.index, 'diff_flux'] = temp_diff

            #新加上diff_flux之后，重新获取白天黑夜的值
            data_D = self.data[Day_Win_Condition]
            data_N = self.data[Night_Win_Condition]
            # 计算MD的数据
            self.data = Method.Md_Method(data_D, data_N, self.data)

            # 计算MAD的数据,新加了一列，所以要重新选值
            data_D = self.data[Day_Win_Condition]
            data_N = self.data[Night_Win_Condition]
            self.data = Method.MAD_Method(data_D, data_N, self.data)


        di_low_range = self.data['flux_Md']-(self.z*self.data['flux_MAD'])/0.6745
        di_high_range = self.data['flux_Md']+(self.z*self.data['flux_MAD'])/0.6745
        # print(di_low_range)
        # print(di_high_range)
        # print(self.data)
        condition = (self.data['diff_flux'] < di_low_range) | \
                    (self.data['diff_flux'] > di_high_range)
        self.data = filter_data.set_data_nan(self.data, condition, self.value)
        # print(self.data)
    # 第三步：存储通量计算
    def StoreFlux(self):
        pass

    # 第四步：摩擦风速筛选
    def Ustar_Threshold(self):
        import step4_ustar_threshold.get_ustar as Get_Ustar

        Get_Ustar.Average_Check(self.data, self.value)

        #将u*<u*c的数据剔除
        condition = (self.data['ustar'] < 0.18) & (self.data['daytime'] == 0)
        self.data = filter_data.set_data_nan(self.data, condition, self.value)

    # 第五步：插补缺失值
    def Gap_Fill(self):
        #线性内插法，interval默认为4
        import step5_gap_fill.linear_insert as linear_insert
        import step5_gap_fill.MDT as MDT
        import step5_gap_fill.light_response as LR
        self.data = linear_insert.linear_insert_method(self.data, self.value)
        # print(self.data)

        # #白天的条件
        Day_Condition = (self.data['daytime'] == 1)
        # 夜晚的筛选条件
        Night_Condition = (self.data['daytime'] == 0)

        #MDT 方法补全
        # 白天的筛选条件
        self.data = MDT.MDT(self.data, Day_Condition, self.value, interval=384)
        # 夜晚的筛选条件
        self.data = MDT.MDT(self.data, Night_Condition, self.value, interval=384)
        # print(self.data)

        #light_response 方法补全
        # self.data = LR.light_response(self.data, Day_Condition, self.value, x_value='PAR_dn_Avg', interval=1000)


if __name__ == '__main__':


    file_path = 'data/'

    # CO2通量数据读入
    #CO2通量数据文件名:yc_1_flux_2012.xls
    CO2_file_name = 'yc_1_flux_2012.xls'
    #CO2_col_names：该文件中需要取出来的列的名称
    CO2_col_names = [
        'date', 'time',
        'DOY', 'daytime',
        'u*', 'co2_flux'
    ]
    a = datetime.now()


    CO2_data = opt_data.file_read_data(CO2_col_names, file_path, CO2_file_name)

    # 气象数据读入
    # CO2通量数据文件名:yc_1_met_2012.xls
    met_file_name = 'yc_1_met_2012.xls'
    # CO2_col_names：该文件中需要取出来的列的名称
    met_col_names = [
        'TIMESTAMP', 'PAR_dn_Avg', 'Slr_Avg'
    ]
    met_data = opt_data.file_read_data(met_col_names, file_path, met_file_name)

    # print(type(met_data['TIMESTAMP'][1]))
    # print(met_data['TIMESTAMP'][1])
    # print(met_data['TIMESTAMP'][1].year)
    # print(met_data['TIMESTAMP'][1].month)
    # print(met_data['TIMESTAMP'][1].day)
    # print(met_data['TIMESTAMP'][1].hour)
    # print(met_data['TIMESTAMP'][1].minute)
    # print(met_data['TIMESTAMP'][1].second)


    plt.figure(figsize=(16, 8))
    # print('import data:', datetime.now() - a)
    # a = datetime.now()
    data_obj = CleanData(CO2_data, met_data, CO2_file_name, value='co2_flux')
    data_obj.check_range(flux_down_range=-20.0, flux_up_range=20.0)
    # plt.scatter(range(data_obj.data.shape[0]), data_obj.data[data_obj.value], label='check_range', s=6)
    # print('check range:', datetime.now() - a)
    # a = datetime.now()
    data_obj.despiking()
    # plt.scatter(range(data_obj.data.shape[0]), data_obj.data[data_obj.value], label='despiking', s=6)
    # print('despiking data:', datetime.now() - a)
    # a = datetime.now()
    data_obj.Ustar_Threshold()
    # plt.scatter(range(data_obj.data.shape[0]), data_obj.data[data_obj.value], label='Ustar_Threshold', s=6)
    # print('Ustar_Threshold data:', datetime.now() - a)
    # a = datetime.now()
    data_obj.Gap_Fill()
    print('Gap_Fill data:', datetime.now() - a)
    plt.scatter(range(data_obj.data.shape[0]), data_obj.data[data_obj.value], label='Gap_Fill', s=6)
    plt.legend()
    plt.show()

    # a = dbopt.DB()
    # data_obj.data.to_sql('test', a.engine, schema=a.schema)



