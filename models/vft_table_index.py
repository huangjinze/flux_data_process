from sqlalchemy import (Column, String, DateTime, UnicodeText, BigInteger, Boolean, Integer, Text, Float)
from sqlalchemy.ext.declarative import declarative_base
import init_data.opt_database as optdb

Base = declarative_base()
class Vft_table_index(Base):
    __tablename__ = 'vft_table_index'
    id = Column(Integer, primary_key=True)
    table_name = Column(String(20))
    index_name = Column(String(20))



def insert(table_name, year, index_names):
    '''
    insert value into vft_table_index
    :param table_name: <string>the name of table stored index
    :param year: <int>the data's year
    :param index_names: <list>index_names
    '''
    db = optdb.DB()
    db.engine.execute(
        Vft_table_index.__table__.insert(),
        [{"table_name": table_name, "year": year, "index_name": i} for i in index_names]
    )
    db.sess.close()




