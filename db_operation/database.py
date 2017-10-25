from sqlalchemy import *
import pandas as pd
from sqlalchemy.orm import *
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
        try:
            self.engine = create_engine(
                'postgresql://{self.user}:{self.password}@localhost:{self.port}/{self.dbname}'.format(**locals()))
            self.con = self.engine.connect()

        except ImportError:
            raise RuntimeError()
        self.metadata = MetaData(self.engine)  # 绑定元信息


    def create_table(self, table_name):
        table = Table(
            table_name,
            self.metadata,
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
        :return:
        '''
        for i in range(len(columns)):
            sql = 'alter table '+table_name+' add '+columns[i]+' '+column_type[i]
            self.engine.execute(sql)
            print(sql)

    def insert(self, data, table_name):
        data = pd.DataFrame(data)
        data.to_sql(table_name, self.engine, schema=self.schema)
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def dump(self):
        pass
if __name__ == '__main__':
    import help
    a = DB()
    # a.create_schema('test')
    # column_type = ['datetime64[ns]', 'float64', 'object', 'float64', 'float64',
    #               'datetime64[ns]', 'float64', 'float64', 'int64']
    # columns = ['date_time', 'DOY', 'daytime', 'co2_flux', 'ustar', 'TIMESTAMP', 'PAR_dn_Avg', 'Slr_Avg', 'windowID']
    # col_type = help.df2sql_dtype(column_type)
    # a.add_column(columns, col_type, 'test')
