import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

if __name__ == '__main__':

    a = datetime.now()
    for i in range(10):
        print('a')
    print(datetime.now() - a)
    # dataset = pd.read_excel(
    #     'data/yc_1_2012_QAQC.xlsx',
    #             header=0,
    #             usecols=['CO2_filled_nlm'],
    #             skiprows=[1]
    #         )
    #
    # plt.figure(figsize=(16, 4))
    # plt.scatter(range(dataset.shape[0]), dataset['CO2_filled_nlm'], label='Gap_Fill',color='r')
    #
    # plt.legend()
    # plt.show()
