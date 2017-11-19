import numpy as np
import pandas as pd

class LinearInsert:
    def linear_insert_method(self, data, value, li_interval):
        temp = data[value]
        temp = temp.interpolate(time=li_interval, limit=int(li_interval/2), limit_direction='both')
        data[value] = temp
        return data



if __name__ == '__main__':
    data = pd.DataFrame({
        # 'windowID': [1, 1, 1, 2, 2, 2, 2],
        # 'co2_flux': [11, 24, 11, 99, 123, 41, 53],
        'num2': [-11, -11, np.nan, -102, np.nan, np.nan, -53,
                 np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,
                 np.nan,87,np.nan,np.nan,900],
        # 'daytime': [0, 0, 1, 1, 0, 0, 0]
    })
    temp = data

    interval = 4
    q = temp['num2'].interpolate(time=interval, limit=2, limit_direction='both')
    gap_data = data[data['num2'].isnull().values==True]
    gap_list = gap_data.index.tolist()
    print(gap_list)
    print(q)
    # interval = 4
    # Linear_list = []
    # for i in range(len(gap_list)-1):
    #     # 如果这个缺失值只是小部分时间缺失，则可以采用线性内插法
    #     if (gap_list[i]+1 < gap_list[i+1] and gap_list[i]+interval>gap_list[i+1]):
    #         Linear_list.append(gap_list[i])
    #     # 如果这个缺失值是连续缺失值，则判断连续的个数有没有超过四个
    #     elif gap_list[i]+1 == gap_list[i+1]:
    #         pass
    #         # flag +=1


    # for i in range(0, len(temp), interval):
    #     current_data = temp[i: i+interval]
    #     # 说明有缺失值，可以调用线性内插法进行填补
    #     if current_data['num2'].count() < interval:
    #         print(current_data.interpolate(method='values'))
