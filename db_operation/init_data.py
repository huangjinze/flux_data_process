import pandas as pd
from sqlalchemy import *
from sqlalchemy.orm import *



# user = 'postgres'
# password = 'root'
# port = '5432'
# dbname = 'demo'
#
# engine = create_engine('postgresql://{user}:{password}@localhost:{port}/{dbname}'.format(**locals()))
# metadata = MetaData(engine)  # 绑定元信息
# users_table = Table('users', metadata, autoload=True)
#
# session = create_session()
#
# class User(object):
#
#     def __repr__(self):
#         return '%s(%r, %r)' % (self.__class__.__name__, self.id, self.name)
#
# class Role(object):
#
#     def __repr__(self):
#         return '%s(%r, %r)' % (self.__class__.__name__, self.id, self.name)
#
# mapper(User, users_table)  # 创建映射
# query = session.query(User)
# u = query.filter_by(email='123@qq.com').first()
# print(u)

def window(data, day_size=13):
    '''
    添加一列,window标签序号,如果最后一个的个数不够window_size的，则算前一个window

    '''
    window_size = day_size * 48
    window_nums = data.shape[0] // window_size
    data['windowID'] = data.index // window_size
    if data.shape[0] % window_size != 0:
        condition = (data.windowID == window_nums)
        data.loc[condition, 'windowID'] = window_nums - 1

    return data


def join_data(flux_data, met_data):
    data = pd.merge(
        flux_data, met_data,
        how='right', left_on='date_time', right_on='TIMESTAMP'
    )

    return data


def file_read_data(col_names, file_path, file_name):
    '''
    从文件读取数据
    :param col_names: 需要读取数据的列的名字
    :param file_path: 文件的路径
    :param file_name: 文件的名字
    :return: 指定列的数据，dataframe格式
    '''
    # yc_1_flux_2012中读取数据，要将date和time字合并
    if file_name.find('yc_1_flux') >= 0:
        dataset = pd.read_excel(
            file_path + file_name,
            header=0,
            usecols=col_names,
            parse_dates=[['date', 'time']],
            skiprows=[1]
        )
    # 否则的话是读的气象数据，不需要合并date和time字段
    elif file_name.find('yc_1_met') >= 0:
        dataset = pd.read_excel(
            file_path + file_name,
            header=0,
            usecols=col_names,
            skiprows=[1]
        )
    else:
        dataset = pd.read_excel(
            file_path + file_name,
            header=0,
            usecols=col_names,
            skiprows=[1]
        )

    data = pd.DataFrame(dataset)
    data.rename(columns={'u*': 'ustar'}, inplace=True)
    return data

def db_read_data(col_names, table_name):
    '''
    从数据库中读取数据
    :param col_names: 需要读取数据的列的名字
    :param table_name: 指定读取数据的数据表
    :return: 指定列的数据，dataframe格式
    '''
    pass

def db_save_data(data, table_name):
    '''
    save data to database
    :param data:
    :param table_name:
    :return:
    '''

def read_conf(filename):
    import configparser
    import json
    import os

    cf = configparser.ConfigParser()

    # cf.read("config/dataConfig.json")
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

if __name__ == '__main__':
    read_conf('config/yc_1_conf.json')