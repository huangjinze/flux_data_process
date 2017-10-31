import filter_data
# 第一步:check range，检查范围，因站点和变量而异

def check_range(
        data, value, tower_name,
        flux_down_range=-20.0, flux_up_range=20.0
):
    '''
    :param data: 读入的原始数据
    :param value: 需要清洗的指标
    :param tower_name: 站点的名称
    :param flux_down_range: 各个通量的上限
    :param flux_up_range: 各个通量的下限
    :return:
    '''
    # 如果是盐池一号

    if tower_name.find('yc_1') >= 0:
        condition = (data[value] < flux_down_range) | (data[value] > flux_up_range)
        data = filter_data.set_data_nan(data, condition, value)
        return data