def df2sql_dtype(columns):
    '''
    dataframe格式的数据类型转成postgresql所能够接受的数据类型
    :param columns: df中的数据列名称, list类型
    :return: postgresql可接受的数据列名称
    '''
    sql_col = []
    for i in columns:
        if i.find('datetime') >= 0:
            sql_col.append('timestamp')
        elif i.find('float') >= 0:
            sql_col.append('float')
        elif i.find('int') >= 0:
            sql_col.append('integer')
        elif i.find('object') >= 0:
            sql_col.append('char')
    return sql_col

if __name__ == '__main__':
    column_type = ['datetime64[ns]', 'float64', 'object', 'float64', 'float64',
                   'datetime64[ns]', 'float64', 'float64', 'int64']

    print(df2sql_dtype(column_type))