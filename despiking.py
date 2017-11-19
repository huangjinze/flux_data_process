import despiking_function.using_function as despike_Method
import init_data.opt_filedata as optdata
import init_data.opt_database as optdb
import filter_data

z=4
ctype='par'
threshold=5
table_name = '2012_yc_1_check_range'
values = ['co2_flux', 'LE', 'H']
# 从数据库中读取数据
db = optdb.DB()
data = db.db_read_data(table_name)


# 如果LT存在的话，则计算ET值
data = despike_Method.calculate_ET(data)


# 进行白天黑夜判断，采用PAR的方法
data = despike_Method.judge_d_n(ctype, data, threshold)

# 给data加上window的标签
data, window_size, window_nums = optdata.window(data, day_size=13)

# 根据每个window的值计算对应的MAD和Md
for i in range(0, window_nums):
    # window i 白天的数据
    Day_Win_Condition = (data['windowID'] == i) & (data['daytime'] == 1)
    Night_Win_Condition = (data['windowID'] == i) & (data['daytime'] == 0)
    data_D = data[Day_Win_Condition]
    data_N = data[Night_Win_Condition]
    for value in values:
        # 对白天CO2_flux进行通量差分计算
        temp_diff = despike_Method.calculate_Diff(data_D, value)
        data.loc[temp_diff.index, value+'_diff'] = temp_diff

        # # 对夜晚CO2_flux进行通量差分计算
        temp_diff = despike_Method.calculate_Diff(data_N, value)
        data.loc[temp_diff.index, value+'_diff'] = temp_diff

        # 新加上diff_flux之后，重新获取白天黑夜的值
        data_D = data[Day_Win_Condition]
        data_N = data[Night_Win_Condition]
        # 计算MD的数据
        data = despike_Method.md_Method(data_D, data_N, data, value)

        # 计算MAD的数据,新加了一列，所以要重新选值
        data_D = data[Day_Win_Condition]
        data_N = data[Night_Win_Condition]
        data = despike_Method.MAD_Method(data_D, data_N, data, value)
for value in values:
    di_low_range = data[value+'_Md']-(z*data[value+'_MAD'])/0.6745
    di_high_range = data[value+'_Md']+(z*data[value+'_MAD'])/0.6745

    condition = (data[value+'_diff'] < di_low_range) | (data[value+'_diff'] > di_high_range)
    data = filter_data.set_data_nan(data, condition, value)


data = despike_Method.calculate_G(data)


db = optdb.DB()
table_name = '2012_yc_1_despiking'
try:
    db.drop(table_name)
    data.to_sql(table_name, db.engine, schema=db.schema)
except:
    data.to_sql(table_name, db.engine, schema=db.schema)

