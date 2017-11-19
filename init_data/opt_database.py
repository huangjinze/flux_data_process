from sqlalchemy import orm
import pandas as pd
from sqlalchemy import *
from sqlalchemy.schema import CreateTable
from os.path import dirname


class DB(object):
    def __init__(self):
        '''
        :param user: postgres
        :param password: root
        :param port: 5432
        :param dbname: demo
        '''
        self.user = 'postgres'
        self.password = 'root'
        self.port = '5432'
        self.dbname = 'demo'
        self.schema = 'public'
        DSNs = {
           'postgresql': 'postgresql://{self.user}:{self.password}@localhost:{self.port}/{self.dbname}'.format(**locals())
        }
        try:
            engine = create_engine(DSNs['postgresql'])
        except ImportError:
            raise RuntimeError()

        try:
            self.con = engine.connect()
        except:
            engine = create_engine(DSNs['postgresql'])

        self.engine = engine
        Session = orm.sessionmaker(bind=engine)
        self.sess = Session()



    def create_table(self, table_name):
        metadata = MetaData(self.engine)  # 绑定元信息
        table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            schema=self.schema
        )
        obj = CreateTable(table)
        self.engine.execute(obj)


    def add_column(self, columns, column_type, table_name):
        '''
        增加数据库的列
        :param columns: list类型，列名称
        :param column_type: list类型，列属性
        :param table_name:数据库表名
        '''
        for i in range(len(columns)):
            sql = 'alter table '+table_name+' add '+columns[i]+' '+column_type[i]
            self.engine.execute(sql)
            print(sql)

    def insert(self, data, table_name):

        pass

    def update(self):
        pass

    def drop(self, table_name):
        '''
        删除数据库
        :param table_name: 数据表名称
        :return:
        '''
        sql = 'drop table "' + table_name+'"'
        self.engine.execute(sql)

    def db_read_data(self, table_name):
        '''
            从数据库中读取数据
            :param col_names: 需要读取数据的列的名字
            :param table_name: 指定读取数据的数据表
            :return: 指定列的数据，dataframe格式
        '''
        data = pd.read_sql_table(table_name, self.con, index_col='index')
        return data

if __name__ == '__main__':
    a = DB()
    data = a.db_read_data('2012yc_1_check_range')
    print(data)
