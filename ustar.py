import ustar_threshold.get_ustar as Get_Ustar
import filter_data
import init_data.opt_database as optdb

table_name = '2012_yc_1_check_range'
value = 'co2_flux'
ustarc = 0.18
# 从数据库中读取数据
db = optdb.DB()
data = db.db_read_data(table_name)

FC1_x, FC1, FC2_x, FC2 = Get_Ustar.Average_Check(data, value)
#将u*<u*c的数据剔除
# condition = (data['ustar'] < ustarc) & (data['daytime'] == 0)
# data = filter_data.set_data_nan(data, condition, value)

import matplotlib.pyplot as plt
print(len(FC1))
print(len(FC2))
ax = plt.figure()
plt.scatter(FC1_x, FC1, label='FC1')
plt.scatter(FC2_x, FC2, label='FC2')
plt.legend()
plt.show()