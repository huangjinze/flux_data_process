import step1_check_range.check_range as cr
import db_operation.init_data as optdata
import db_operation.database as optdb

file_path = 'data/'
conf_path = 'config/'
tower_name = 'yc_1'
year = '2012'
conf = optdata.read_conf(conf_path+tower_name+'_conf.json')

# CO2通量数据读入
# CO2通量数据文件名:yc_1_flux_2012.xls
flux_file_name = 'yc_1_flux_2012.xls'
# CO2_file_name = 'yc_1_flux_test.xls'
# CO2_col_names：该文件中需要取出来的列的名称

flux_data_names = ['co2_flux', 'H', 'LE']
flux_col_names = ['date', 'time', 'DOY', 'daytime', 'u*']
flux_names = flux_col_names + flux_data_names
flux_data = optdata.file_read_data(flux_names, file_path, flux_file_name)


# 气象数据读入
# flux通量数据文件名:yc_1_met_2012.xls
met_file_name = 'yc_1_met_2012.xls'
# met_file_name = 'yc_1_met_test.xls'
# CO2_col_names：该文件中需要取出来的列的名称
met_data_name = ['soilG_1_Avg', 'soilG_2_Avg', 'soilG_3_Avg', 'soilG_4_Avg', 'soilG_5_Avg']
met_col_names = ['TIMESTAMP', 'PAR_dn_Avg', 'Slr_Avg']
met_data = optdata.file_read_data(met_col_names, file_path, met_file_name)

data_obj = optdata.join_data(flux_data, met_data)

for i in flux_data_names:
    data_obj = cr.check_range(
        data_obj, i, tower_name,
        flux_down_range=conf[i]['Low'], flux_up_range=conf[i]['High'])
a = optdb.DB()
table_name = year+tower_name+'_check_range'
try:
    a.drop(table_name)
    data_obj.to_sql(table_name, a.engine, schema=a.schema)
except:
    data_obj.to_sql(table_name, a.engine, schema=a.schema)
