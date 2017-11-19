import gap_fill.method as gapMethod
import init_data.opt_database as optdb

table_name = '2012_yc_1_despiking'
value_co2 = ['co2_flux']
value_power = ['Rn_Avg', 'H', 'LE', 'G']
# 从数据库中读取数据
db = optdb.DB()
data = db.db_read_data(table_name)

method = gapMethod.Facade()
# self.data = method.MethodA(self.data, self.value)
# print(self.data)
method.MethodB(data, value_co2, x_lr_value='PAR_net_Avg', x_tr_value=['soil_T_1_10cm_Avg', 'Ta_Avg'])