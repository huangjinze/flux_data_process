import step5_gap_fill.linear_insert as LI
import step5_gap_fill.MDT as MDT
import step5_gap_fill.light_response as LR
# import step5_gap_fill.temperature_response as TR

class Facade:
    def __init__(self):
        self.linear_insert = LI.LinearInsert()
        self.mdt = MDT.MDT()
        self.lr = LR.LightResponse()
        # self.tr = TR()
    def MethodA(self, data, value, li_interval=4, mdt_interval=384):
        '''
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


    def MethodB(self, data, value, li_interval=4, x_value='par'):
        print("linear insert + light response:")

        data = self.linear_insert.linear_insert_method(data, value, li_interval)

        # #白天的条件
        Day_Condition = (data['daytime'] == 1)
        data = self.lr.light_response(data, Day_Condition, value, x_value)

        # 夜晚的筛选条件
        Night_Condition = (data['daytime'] == 0)
    #     self.three.MethodThree()