import pandas as pd
from sqlalchemy import *
from sqlalchemy.orm import *



user = 'postgres'
password = 'root'
port = '5432'
dbname = 'demo'

engine = create_engine('postgresql://{user}:{password}@localhost:{port}/{dbname}'.format(**locals()))
metadata = MetaData(engine)  # 绑定元信息
users_table = Table('users', metadata, autoload=True)

session = create_session()

class User(object):

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.id, self.name)

class Role(object):

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.id, self.name)

mapper(User, users_table)  # 创建映射
query = session.query(User)
u = query.filter_by(email='123@qq.com').first()
print(u)





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