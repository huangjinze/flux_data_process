import check_range.check_range as cr
import init_data.opt_filedata as optdata
import init_data.opt_database as optdb
import pandas as pd
import models.vft_table_index as vti
# file_path = 'data/'
# conf_path = 'config/'
# tower_name = 'yc_1'
# flux_file_name = 'yc_1_flux_2012.xls'
#
# dataset = pd.read_excel(
#             file_path + flux_file_name,
#             header=0,
#             parse_dates=[['date', 'time']],
#             skiprows=[1]
#         )
# index = dataset.columns.values.tolist()
# index = ['date_time', 'filename', 'DOY', 'daytime', 'H', 'LE', 'co2_flux', 'u*', 'file_records', 'used_records', 'Tau', 'qc_Tau', 'qc_H', 'qc_LE', 'qc_co2_flux', 'h2o_flux', 'qc_h2o_flux', 'H_strg', 'LE_strg', 'co2_strg', 'h2o_strg', 'co2_v-adv', 'h2o_v-adv', 'co2_molar_density', 'co2_mole_fraction', 'co2_mixing_ratio', 'co2_time_lag', 'co2_def_timelag', 'h2o_molar_density', 'h2o_mole_fraction', 'h2o_mixing_ratio', 'h2o_time_lag', 'h2o_def_timelag', 'sonic_temperature', 'air_temperature', 'air_pressure', 'air_density', 'air_heat_capacity', 'air_molar_volume', 'water_vapor_density', 'e', 'es', 'specific_humidity', 'RH', 'VPD', 'Tdew', 'u_unrot', 'v_unrot', 'w_unrot', 'u_rot', 'v_rot', 'w_rot', 'wind_speed', 'max_wind_speed', 'wind_dir', 'yaw', 'pitch', 'roll', 'TKE', 'L', '(z-d)/L', 'bowen_ratio', 'T*', 'model', 'x_peak', 'x_offset', 'x_10%', 'x_30%', 'x_50%', 'x_70%', 'x_90%', 'un_Tau', 'Tau_scf', 'un_H', 'H_scf', 'un_LE', 'LE_scf', 'un_co2_flux', 'co2_scf', 'un_h2o_flux', 'h2o_scf', 'spikes', 'amplitude_resolution', 'drop_out', 'absolute_limits', 'skweness_kurtosis', 'skweness_kurtosis.1', 'discontinuities', 'discontinuities.1', 'timelag', 'timelag.1', 'attack_angle', 'non_steady_wind', 'u_spikes', 'v_spikes', 'w_spikes', 'ts_spikes', 'co2_spikes', 'h2o_spikes', 'u_var', 'v_var', 'w_var', 'ts_var', 'co2_var', 'h2o_var', 'w/ts_cov', 'w/co2_cov', 'w/h2o_cov', 'co2_mean', 'h2o_mean', 'co2_mean.1', 'h2o_mean.1', 'dew point_mean']
# print(type(dict({'index_name': index})))
# print(dict({'index_name': index}))
index = {
    'table_name': 'yc_1_fluxs',
    'index_name': 'date_time'
}
new_vti = vti.Vft_table_index(table_name='yc_1_fluxs', index_name='date_time')
db = optdb.DB()
db.sess.add(new_vti)
db.sess.commit()
db.sess.close()