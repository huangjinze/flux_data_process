import check_range.check_range as cr
import init_data.opt_filedata as optdata
import init_data.opt_database as optdb
import models.vft_table_index as models_vti

file_path = 'data/'
conf_path = 'config/'
tower_name = 'yc_1'
year = '2012'

# CO2通量数据文件名:yc_1_flux_2012.xls
flux_file_name = 'yc_1_flux_2012.xls'
# CO2_file_name = 'yc_1_flux_test.xls'
# CO2_col_names：该文件中需要取出来的列的名称

flux_data_names = ['co2_flux', 'H', 'LE', 'u*']
flux_col_names = ['date', 'time', 'DOY', 'daytime']

# flux通量数据文件名:yc_1_met_2012.xls
met_file_name = 'yc_1_met_2012.xls'
# met_file_name = 'yc_1_met_test.xls'
# CO2_col_names：该文件中需要取出来的列的名称
met_data_names = ['PAR_net_Avg', 'Rn_Avg', 'soilG_1_Avg', 'soilG_2_Avg', 'soilG_3_Avg', 'soilG_4_Avg', 'soilG_5_Avg']
met_col_names = ['TIMESTAMP', 'Slr_Avg']




conf = optdata.read_conf(conf_path+tower_name+'_conf.json')

# CO2通量数据读入
flux_names = flux_col_names + flux_data_names
flux_data = optdata.file_read_data(flux_names, file_path, flux_file_name)

# # 气象数据读入
met_names = met_col_names + met_data_names
met_data = optdata.file_read_data(met_names, file_path, met_file_name)

# 在读入数据之后，flux_data中列名重命名为ustar，
# 重新检查flux_data_names U*是否存在，存在的话需要替换成ustar
flux_data_names = ['ustar' if x=='u*' else x for x in flux_data_names]

process_data = flux_data_names + met_data_names
data_obj = optdata.join_data(flux_data, met_data)

for i in process_data:
    if i in conf:
        print(i)
        data_obj = cr.check_range(
            data_obj, i, tower_name,
            flux_down_range=conf[i]['Low'], flux_up_range=conf[i]['High'])

db = optdb.DB()
table_name = year+'_'+tower_name+'_check_range'
models_vti.insert(table_name, year, flux_names+met_names)

try:
    db.drop(table_name)
    data_obj.to_sql(table_name, db.engine, schema=db.schema)
except:
    data_obj.to_sql(table_name, db.engine, schema=db.schema)
db.sess.close()
