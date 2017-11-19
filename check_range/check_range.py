import filter_data

def check_range(
        data, value, tower_name,
        flux_down_range=-20.0, flux_up_range=20.0
):
    '''
    :param data: original data
    :param value: index needed to be cleaned
    :param tower_name: tower name
    :param flux_down_range: flux down range
    :param flux_up_range: flux up range
    :return:
    '''

    if tower_name.find('yc_1') >= 0 :
        condition = (data[value] < flux_down_range) | (data[value] > flux_up_range)
        data = filter_data.set_data_nan(data, condition, value)
        return data