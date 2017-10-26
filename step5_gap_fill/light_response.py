import numpy as np
import pandas as pd
from scipy import optimize
from scipy import stats
# import statsmodels.api as sm

def func(PAR, p):
    '''
    co2_flux = a*b*PAR/(a*PAR+b)+c
    :param x: 自变量
    :param p: 参数
    :return: 函数计算结果
    '''
    a, b, c = p
    return a*b*PAR/(a*PAR+b)+c
    # return a*np.sin(2*np.pi*b*PAR+c)

def residuals(p, y, x):
    '''
    实验数据x, y 和拟合函数之间的差，p为需要找到的系数
    :param p:
    :param y:
    :param x:
    :return:
    '''
    return y - func(x, p)

def get_lift_time(data, y_value, x_value, interval=1000):
    '''
    :param data: 白天的数据
    :param y_value: 待插补的数据因变量名称:co2_flux
    :param x_value: 待插补的数据自变量名称:PAR
    :param interval:  参考的时间间隔
    :return: 生长季开始时间
    '''
    # for i in data.index.tolist():
    for i in [1]:
        p0 = [7, 0.4, 0.1]
        y = data.iloc[i:i+interval+1][y_value]
        x = data.iloc[i:i+interval+1][x_value]
        # print(type(x))
        # print(type(y))
        plsq = optimize.leastsq(residuals, p0, args=(y, x))
        #检验p的值
        t, p = stats.ttest_1samp(func(x, plsq[0]), np.mean(y))
        if p >= 0.95:
            print(i)

def light_response(data, condition, y_value, x_value, interval=1000):
    '''
    先要找到生长季开始的时间
    :param data: 总的数据集合
    :param condition: 数据的限制条件
    :param y_value: 待插补的数据因变量:co2_flux
    :param x_value: 待插补的数据自变量:PAR
    :param interval: 参考的时间间隔
    :return: 插补后的数据集合
    '''
    # 白天的数据重新设置索引，然后找出相应np.nan的数据
    temp_data = data[condition].set_index([list(range(len(data[condition])))])
    get_lift_time(data, y_value, x_value, interval=1000)

    # 筛选的条件
    Condition = (temp_data[y_value].isnull().values == True)
    # 缺失值的索引
    var_index = temp_data[Condition].index.tolist()

if __name__ == '__main__':


    # x = np.linspace(0, 2*np.pi, 100)
    # A, k, theta = 10, 0.34, np.pi/6 #真实数据的函数参数
    # y0 = func(x, [A, k, theta])#真实数据
    # #加入噪声之后的实验数据
    # np.random.seed(0)
    # y1 = y0 + 1 * np.random.randn(len(x))
    #
    # p0 = [7, 0.4, 0]#第一次猜测函数的拟合参数
    #
    # #调用leastsq进行数据拟合
    # #residuals为计算误差的函数
    # #p0为拟合参数的初始值
    # #args = 拟合的实验数据
    # plsq = optimize.leastsq(residuals, p0, args=(y1, x))
    #
    # print(np.nanmean(y0))
    # print([A, k, theta])
    # print(plsq)
    # t, p =stats.ttest_1samp(y1, np.mean(y0))
    # if p>=0.5:
    #     print('aaa', p)

    # df = pd.DataFrame(np.random.randn(6, 4), columns=list('abcd'))
    # print(df)
    # print(df.iloc[2:4]['a'],)

    x= \
        [0.037, 0.041, 0.042, 0.047, 0.053, 0.035, 0.048, 0.032, 0.042, 0.043, 0.04, 0.034, 0.048, 0.051, 0.041, 1.155,
         25.83, 97.20002, 213.0, 328.6, 479.6, 614.8, 740.8, 848.0, 925.0, 951.0, 962.0, 930.0, 870.0, 768.0, 687.3,
         490.6, 349.2, 197.4, 72.65, 10.32, 0.154, 0.055, 0.077, 0.072, 0.07, 0.078, 0.062, 0.041, 0.034, 0.043, 0.071,
         0.063, 0.05, 0.058, 0.055, 0.061, 0.062, 0.054, 0.048, 0.048, 0.032, 0.042, 0.034, 0.03, 0.04, 0.05, 0.053,
         0.804, 21.29, 80.4, 172.1, 330.4, 434.4, 478.3, 657.0, 650.8, 708.7, 767.3, 930.0, 915.0, 594.9, 738.3, 659.7,
         540.2, 262.3, 163.3, 62.37, 7.748, 0.096, 0.024, 0.018, 0.04, 0.034, 0.046, 0.029, 0.033, 0.045, 0.041, 0.055,
         0.066, 0.058, 0.035, 0.032, 0.022, 0.035, 0.057, 0.049, 0.037, 0.026, 0.023, 0.017, 0.029, 0.023, 0.035, 0.041,
         0.583, 15.86, 67.84, 134.0, 224.6, 327.4, 441.3, 552.5, 763.3, 896.0, 937.0, 937.0, 942.0, 946.0, 852.0, 731.1,
         599.0, 442.1, 276.2, 112.2, 14.39, 0.178, 0.019, 0.023, 0.03, 0.023, 0.034, 0.039, 0.048, 0.024, 0.04, 0.041,
         0.041, 0.032, 0.065, 0.034, 0.037, 0.037, 0.019, 0.021, 0.024, 0.037, 0.019, 0.023, 0.024, 0.032, 0.03, 0.039,
         1.251, 26.66, 103.1, 243.8, 405.3, 550.5, 687.1, 800.0, 890.0, 952.0, 982.0, 986.0, 960.0, 913.0, 829.0, 715.4,
         580.3, 418.1, 252.4, 96.5, 13.91, 0.19, 0.035, 0.033, 0.017, 0.016, 0.019, 0.019, 0.021, 0.022, 0.022, 0.048,
         0.052, 0.033, 0.04, 0.03, 0.049, 0.042, 0.035, 0.023, 0.032, 0.014, 0.031, 0.023, 0.023, 0.039, 0.022, 0.024,
         0.966, 24.05, 97.3, 216.0, 351.7, 483.9, 613.3, 725.3, 819.0, 885.0, 921.0, 929.0, 906.0, 854.0, 765.7, 658.6,
         521.7, 366.8, 218.1, 83.6, 13.46, 0.182, 0.014, 0.023, 0.017, 0.021, 0.018, 0.027, 0.031, 0.029, 0.025, 0.027,
         0.04, 0.032, 0.029, 0.033, 0.029, 0.027, 0.027, 0.025, 0.047, 0.037, 0.025, 0.026, 0.014, 0.037, 0.052, 0.041,
         0.811, 21.84, 89.4, 198.0, 334.0, 466.6, 556.2, 668.6, 769.9, 813.0, 833.0, 830.0, 822.0, 744.4, 675.6, 565.9,
         436.4, 291.0, 154.3, 62.05, 11.03, 0.203, 0.053, 0.062, 0.072, 0.072, 0.104, 0.094, 0.09, 0.097, 0.083, 0.079,
         0.087, 0.09, 0.08, 0.069, 0.053, 0.073, 0.034, 0.03, 0.058, 0.051, 0.051, 0.04, 0.034, 0.051, 0.059, 0.046,
         0.916, 22.08, 86.20002, 157.2, 258.1, 348.4, 534.0, 559.6, 564.5, 733.9, 805.0, 883.0, 839.0, 783.0, 660.2,
         582.6, 397.1, 401.8, 217.1, 67.36999, 12.77, 0.247, 0.025, 0.016, 0.025, 0.043, 0.021, 0.025, 0.029, 0.029,
         0.026, 0.034, 0.022, 0.053, 0.029, 0.031, 0.027, 0.061, 0.035, 0.032, 0.021, 0.021, 0.034, 0.039, 0.022, 0.022,
         0.027, 0.041, 0.96, 24.37, 101.2, 232.9, 383.0, 525.2, 659.6, 776.9, 869.0, 928.0, 975.0, 978.0, 926.0, 924.0,
         836.0, 656.0, 479.4, 397.5, 193.3, 81.70002, 15.41, 0.336, 0.042, 0.056, 0.054, 0.049, 0.049, 0.027, 0.037,
         0.027, 0.039, 0.032, 0.04, 0.046, 0.03, 0.047, 0.037, 0.045, 0.024, 0.056, 0.042, 0.063, 0.037, 0.032, 0.05,
         0.034, 0.033, 0.041, 0.772, 24.22, 104.6, 189.7, 297.7, 436.5, 501.3, 697.4, 754.5, 796.1, 860.0, 908.0, 898.0,
         895.0, 536.2, 646.9, 535.2, 390.7, 185.8, 82.20002, 15.59, 0.356, 0.014, 0.027, 0.017, 0.046, 0.062, 0.054,
         0.045, 0.045, 0.034, 0.042, 0.045, 0.027, 0.032, 0.034, 0.046, 0.03, 0.042, 0.046, 0.038, 0.038, 0.045, 0.039,
         0.037, 0.022, 0.029, 0.034, 0.837, 29.33, 115.2, 232.9, 355.0, 503.7, 624.6, 645.4, 806.0, 839.0, 811.0, 837.0,
         765.9, 835.0, 707.1, 622.6, 494.5, 388.5, 188.8, 70.88, 15.18, 0.396, 0.03, 0.019, 0.023, 0.039, 0.023, 0.043,
         0.043, 0.041, 0.034, 0.045, 0.019, 0.032, 0.023, 0.03, 0.025, 0.035, 0.037, 0.037, 0.039, 0.023, 0.062, 0.053,
         0.032, 0.035, 0.029, 0.025, 0.911, 23.26, 98.1, 232.8, 383.8, 528.5, 667.2, 788.8, 878.0, 936.0, 972.0, 981.0,
         961.0, 911.0, 830.0, 729.0, 594.9, 455.2, 296.6, 130.5, 23.72, 0.674, 0.029, 0.038, 0.045, 0.047, 0.046, 0.061,
         0.038, 0.055, 0.055, 0.039, 0.055, 0.054, 0.03, 0.024, 0.048, 0.054, 0.067, 0.073, 0.049, 0.048, 0.042, 0.034,
         0.039, 0.037, 0.042, 0.031, 0.875, 23.62, 91.4, 188.9, 330.9, 477.3, 618.2, 733.4, 831.0, 877.0, 954.0, 953.0,
         928.0, 886.0, 814.0, 713.8, 578.4, 428.7, 269.0, 118.7, 22.21, 0.629, 0.03, 0.022, 0.021, 0.029, 0.042, 0.023,
         0.037, 0.041, 0.035, 0.04, 0.039, 0.045, 0.041, 0.04, 0.027, 0.035, 0.035, 0.045, 0.038, 0.021, 0.025, 0.041,
         0.061, 0.05, 0.034, 0.042, 0.842, 22.48, 93.5, 218.1, 372.5, 502.3, 631.7, 750.4, 848.0, 921.0, 961.0, 989.0,
         931.0, 689.8, 550.5, 621.5, 591.0, 389.4, 167.7, 76.18, 14.84, 0.459, 0.059, 0.047, 0.047, 0.038, 0.047, 0.071,
         0.064, 0.057, 0.03, 0.04, 0.03, 0.021, 0.035, 0.009, 0.019, 0.029, 0.024, 0.029, 0.026, 0.027, 0.039, 0.031,
         0.038, 0.029, 0.032, 0.025, 0.745, 21.87, 84.8, 193.8, 288.8, 379.8, 628.3, 633.0, 663.0, 732.2, 769.9, 759.1,
         560.4, 401.8, 331.3, 440.9, 460.0, 280.0, 142.8, 56.56, 13.54, 0.634, 0.067, 0.073, 0.072, 0.055, 0.048, 0.049,
         0.034, 0.026, 0.019, 0.03, 0.037, 0.033, 0.019, 0.031, 0.034, 0.019, 0.018, 0.03, 0.042, 0.025, 0.03, 0.041,
         0.035, 0.041, 0.031, 0.041, 1.109, 26.09, 100.8, 225.0, 371.3, 522.1, 657.8, 780.9, 884.0, 948.0, 986.0, 989.0,
         962.0, 901.0, 813.0, 704.3, 566.4, 408.4, 249.3, 113.1, 26.58, 1.042, 0.054, 0.025, 0.037, 0.021, 0.022, 0.026,
         0.031, 0.035, 0.033, 0.033, 0.031, 0.035, 0.039, 0.041, 0.047, 0.07, 0.055, 0.057, 0.045, 0.041, 0.035, 0.035,
         0.029, 0.046, 0.047, 0.053, 0.759, 18.43, 91.70002, 186.3, 336.2, 346.1, 555.8, 710.9, 810.0, 878.0, 934.0,
         939.0, 932.0, 878.0, 808.0, 697.5, 582.5, 423.6, 244.6, 116.5, 27.23, 1.271, 0.071, 0.055, 0.058, 0.055, 0.042,
         0.064, 0.08, 0.079, 0.109, 0.066, 0.069, 0.045, 0.058, 0.042, 0.065, 0.072, 0.071, 0.069, 0.082, 0.055, 0.051,
         0.049, 0.055, 0.054, 0.058, 0.064, 0.913, 20.05, 87.1, 182.2, 281.0, 372.0, 514.8, 591.5, 739.0, 667.8, 608.9,
         564.6, 771.4, 712.5, 540.1, 428.7, 383.1, 283.3, 227.4, 106.9, 24.57, 1.13, 0.062, 0.066, 0.038, 0.041, 0.051,
         0.061, 0.049, 0.033, 0.059, 0.033, 0.04, 0.029, 0.024, 0.03, 0.034, 0.042, 0.026, 0.025, 0.033, 0.035, 0.03,
         0.032, 0.045, 0.032, 0.043, 0.03, 1.102, 23.69, 100.3, 226.4, 379.9, 539.5, 625.0, 741.5, 782.9, 855.0, 863.0,
         837.0, 694.8, 617.1, 502.4, 541.7, 463.3, 381.7, 234.5, 113.7, 28.02, 1.473, 0.029, 0.042, 0.05, 0.058, 0.067,
         0.054, 0.064, 0.067, 0.087, 0.081, 0.071, 0.063, 0.043, 0.073, 0.065, 0.066, 0.08, 0.057, 0.064, 0.069, 0.047,
         0.07, 0.041, 0.07, 0.071, 0.064, 0.713, 10.36, 37.25, 85.1, 147.7, 233.4, 244.2, 283.6, 277.9, 321.6, 357.6,
         435.3, 348.2, 377.1, 275.6, 256.6, 280.0, 255.1, 171.6, 84.1, 23.92, 1.195, 0.073, 0.065, 0.077, 0.079, 0.071,
         0.069, 0.062, 0.071, 0.058, 0.071, 0.059, 0.063, 0.058, 0.039, 0.045, 0.041, 0.064, 0.07, 0.054, 0.075, 0.048,
         0.057, 0.041, 0.057, 0.047, 0.04, 0.627, 13.32, 52.72, 87.1, 125.9, 173.6, 219.2, 267.4, 310.1, 348.1, 368.4,
         357.8, 389.0, 353.4, 342.9, 347.7, 278.7, 223.2, 170.2, 76.56, 24.0, 1.453, 0.041, 0.042, 0.053, 0.061, 0.048,
         0.07, 0.062, 0.062, 0.067, 0.07, 0.057, 0.058, 0.043, 0.055, 0.053, 0.043, 0.033, 0.037, 0.046, 0.046, 0.042,
         0.032, 0.048, 0.043, 0.026, 0.043, 0.657, 14.04, 64.28, 109.5, 160.7, 240.1, 298.7, 377.5, 439.2, 479.7, 493.4,
         515.8, 534.9, 503.5, 451.7, 398.4, 347.9, 271.8, 186.4, 101.2, 31.79, 2.173, 0.035, 0.025, 0.038, 0.031]

    print(len(x))
    y = \
        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, -2.08320723823546,
         -2.08320723823546, -2.08320723823546, 0.80599349260002, 0.373249690311264, -0.274293100785627,
         0.04818407313379974, 0.3706612470532265, 0.6931384209726532, 1.01561559489208, 0.695218661785429,
         1.33347877362008, 1.09355562332858, 0.531958911172869, 0.6468685332487, 0.328377042995777, -0.109886416946001,
         1.1281809414292, 0.340320433667737, 0.289147539211397, 0.0280044262067068, 0.0274067732203912,
         -0.0738412235686104, -0.161148448258305, -0.202717727398918, 0.106925784709949, 0.192669583364267,
         0.300295296890674, 0.19661410761066797, 0.0929329183306619, -0.00979141633509189, -0.249318939647089,
         0.0841159689159876, -0.0443177003750524, -0.356344556634128, -0.152886839003502, 0.0202936020129432,
         -0.272951257573195, -0.0543849607349809, 0.0802331944659617, 0.06024581276506074, 0.040258431064159786, np.nan,
         np.nan, -0.01970371403854307, -0.03969109573944403, -0.059678477440345, -0.05914003868983653,
         -0.058601599939328064, np.nan, -0.05752472243831113, -0.05698628368780266, -0.0564478449372942, 0.161248444476435,
         0.175508959280876, 0.0480469352944189, 0.205429674255574, 0.680141720280962, -0.0307880515700518,
         1.55481835819459, -0.386677595072932, 0.17075140868953, 0.334637505414192, -0.334022877089983,
         0.010821616092955955, 0.355666109275895, -0.310561557257074, -0.23043019723402036, -0.15029883721096673, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.6510147630195696, 0.7311461230426234, 0.811277483065677,
         0.7592372077581524, 0.7071969324506278, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         -0.07340719716224176, -0.1254474724697664, -0.177487747777291, 0.153339352380429, 0.168930672610012,
         0.815487312907185, 2.42750988772736, 0.541104205678757, 0.166644672294215, 0.6249170489746025,
         1.08318942565499, 0.203905661284042, -1.22871318128746, 0.0654070685366169, -0.374805577508306,
         0.167789799623687, -0.493554703799498, -0.460122608862143, -0.426690513924788, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.3088155746970221,
         0.3422476696343771, 0.375679764571732, 0.5918794857892655, 0.808079207006799, np.nan, np.nan, np.nan, 1.672878091876933,
         1.8890778130944665, 2.105277534312, 0.194761059778412, 0.286590674789757, 0.32435801322819, 0.242775166877296,
         0.209806629224703, 0.416340088614739, -0.0109459233005121, -1.03709802890361, -0.5547802509408375,
         -0.0724624729780651, -0.363096419792961, -0.427106004314142, -0.123914530646904, -0.0150804643634969,
         0.673789155103306, 0.6077108444339112, 0.5416325337645165, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, -0.3173855049376155, -0.38346381560701026, -0.449542126276405, -0.4095994862193895,
         -0.36965684616237404, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         0.22948275469285817, 0.2694253947498736, 0.309368034806889, 0.632763295388708, 0.952130929048043,
         0.80048080160852, 0.463244809231601, -0.31341633233904, -0.10862187310441, 0.48586985830769996,
         1.08036158971981, 0.68701944503951, 0.599035960919792, 0.180162256018644, 0.111662026028244,
         0.08201333909608106, 0.05236465216391812, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, -0.8074472688688071, -0.8370959558009701,
         -0.866744642733133, 1.6271376458288, 1.77314257433742, 1.8361943247509, 1.89924607516438, 0.919257070683884,
         0.279565826793427, -0.720336295229414, 0.581070062612796, 0.482275633594103, 0.474352324965049,
         1.16405632911581, -0.261529458053463, -0.0367260145587542, 0.689596759674694, 1.1404151855893,
         0.7111784653973854, 0.28194174520547066, -0.147294974986444, -0.14138322007522, -0.135471465163996,
         -0.118972593731986, -0.102473722299976, np.nan, np.nan, np.nan, np.nan, np.nan, -0.0034804937079160048, 0.013018377724094005,
         0.029517249156104, 0.4140482686752815, 0.798579288194459, 0.0576338799197768, 0.0693246153762872,
         -0.00749652120770971, 0.0875587343937767, 0.17913355828805336, 0.27070838218233, 0.284388925042434,
         0.3920363374651795, 0.499683749887925, -0.0325966084281177, 0.005830586860008841, 0.04425778214813538,
         0.08268497743626191, 0.12111217272438846, 0.159539368012515, 0.134474186095319, 0.21343944112923,
         -0.925642421758695, 0.255207813793868, -1.94048572666321, 0.54804982739431, -0.12113283385743334,
         -0.7903154951091766, -1.45949815636092, 1.95062523230309, 0.837858849039072, -0.86954146330233,
         -0.0476745724456883, 0.795630316641365, 0.470375508485477, 2.62147968848838, 2.510123773694785,
         2.398767858901189, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.8397850517908545,
         0.7284291369972591, 0.617073222203664, 0.5568575866421921, 0.4966419510807201, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, -0.1657300400954711, -0.22594567565694312, -0.286161311218415, 0.151795187767014,
         0.844377628537679, -1.1683460208749, 0.810443240090446, -0.112600392496435, 0.020891000067507492,
         0.15438239263145, -0.0528542109033817, 0.371771867503672, 0.540253431639133, 0.343433509985982,
         -0.0697157575886734, 0.0383673412652775, 0.5364651957007917, 1.034563050136306, 1.53266090457182,
         1.4680211570327717, 1.4033814094937234, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, -0.6004507642167765,
         -0.6650905117558246, -0.729730259294873, 0.65071880334398, 1.44566496313374, 0.600365078750166,
         0.541853639815257, 0.406250624478951, -0.96487710273787, 0.23622194545783, 0.53228506603192,
         -0.764537635590022, -0.620321011915003, -0.633376312521271, -0.5296009179366155, -0.4258255233519598, np.nan, np.nan,
         np.nan, -0.010723945013337288, 0.09305144957131839, 0.196826844155974, 0.403360375145019, 0.382097859486878,
         0.240310967070429, -0.0227156399415544, 0.162416017613785, -0.094243247526845, -0.04639454840620187,
         0.0014541507144412574, 0.049302849835084386, 0.0971515489557275, 0.0376580024243024, 0.0332283832842827,
         -0.0589230122797478, 0.0183031624507606, 0.0223915545571905, 0.00610246902024212, 0.037478617227436416,
         0.0688547654346307, 0.007521121736205255, -0.053812521962220194, np.nan, -0.1764798093590711,
         -0.23781345305749652, -0.299147096755922, -0.285186199510665, -0.27122530226540803, -0.257264405020151,
         0.222806954265491, 0.413284583042755, 0.189526537951649, -0.293563519143184, -0.2111063323808,
         -0.28684518393579, -0.316692568438382, 0.0196593242297278, -0.616603533138558, 0.039988129629236,
         0.0888162358858081, 0.23024249734388402, 0.37166875880196, 1.25893509614932, 1.2150882720243226,
         1.1712414478993252, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, 0.2943049653993778, 0.2504581412743805, 0.206611317149383, 0.09438167248120358, -0.01784797218697584, np.nan,
         np.nan, -0.3545369061915141, -0.46676655085969354, -0.578996195527873, 0.063590466700994, 0.706177128929861,
         -0.048136114914706, 1.28686176693811, -0.103824805366976, 0.438227723363319, -0.0467529109886588,
         -0.0626330176749857, 0.0101844435794531, -0.767002362421796, 0.13421867469146, 0.290929504300018,
         -0.0885005534988642, -0.21126994430298, 0.080608755937866, -0.143570950239908, 0.183708348571103,
         0.122867131944055, 0.1378759012353648, 0.1528846705266746, 0.1678934398179844, 0.18290220910929422,
         0.197910978400604, -0.0344966007145878, -0.0789186141869749, -0.123340627659362, -0.0358875795448732,
         0.023896887284258872, 0.08368135411339095, 0.143465820942523, 0.167197427027098, 0.190929033111673,
         0.214660639196248, 0.238392245280823, 0.262123851365398, -0.246280772005326, -0.148142893651125,
         -0.251797645262717, 0.01714987672614643, 0.28609739871500983, 0.5550449207038732, 0.8239924426927366,
         1.0929399646816, -0.4239305198968, -0.283068613868879, -0.142206707840958, 0.608201280571802,
         0.185389482932394, -1.69202098936636e-05, 0.158397645328523, 0.223801157354098, 0.75536526821888,
         0.4202194649988553, 0.08507366177883069, -0.25007214144119405, -0.5852179446612186, -0.920363747881243,
         -0.49465291414706464, -0.0689420804128863, 0.356768753321292, 1.00150362417644, 1.2119430445616999,
         1.42238246494696, -0.00815441730788651, 1.67313869406081, 1.6205351869190376, 1.567931679777265, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         0.20024049409118239, 0.14763698694940985, 0.0950334798076375, -0.0483429065638105, 0.0785085378261792,
         0.600560132094001, 0.390926302239132, 0.0969573911307765, -0.197011519977579, 0.27516415402902,
         0.904711342862872, 0.0295896511096259, 0.0709465741279286, 0.393440941696715, 0.451355291253174,
         0.370494866893051, 2.1630443249059, 0.315812768127896, 0.287727730524595, -0.785314543179589,
         -0.7508514099441338, -0.7163882767086787, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.38643198682588775,
         0.4208951200613428, 0.455358253296798, 0.49335022781066, 0.409571850711104, -0.694034071761792,
         0.0678180545789652, -0.163812864807417, 0.118392622203033, 0.145478961489428, -0.0467190294120171,
         0.81300831818665, -0.891092729559351, -0.57282843931834, 0.2167130603111, -0.807672949799595,
         0.508412577576703, 0.5095422432788873, 0.5106719089810715, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.5434322143444155,
         0.5445618800465997, 0.545691545748784, 0.191319969862317, 0.224497861159996, 0.38138595266756,
         -0.281258680703099, 0.100861875631885, 0.956910716446431, 0.639604577335447, 0.8244441228883,
         0.481104416630097, 0.711349821814734, 0.376665349663015, 0.267193508190457, 0.27485269457653,
         0.15329957000468603, 0.03174644543284205, -0.0898066791390019, -0.03653965815210124, 0.01672736283479942, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.6026645936907067, 0.6559316146776073, 0.709198635664508,
         -0.537244279235758, -0.54629685740569, -0.555349435575622, -0.564402013745554, -0.450838440079022,
         -0.390940321385935, 0.454413134777233, -0.47386670785337, -0.608933005976939, 0.220932242056913,
         -0.0199083427349789, -0.313398159296197, 0.103028010109546, 0.0857523440518478, -1.61106222851741,
         -0.7847725296368127, 0.04151716924378479, 0.8678068681243822, 1.69409656700498, 1.6475828427644599,
         1.60106911852394, 0.8139045328604635, 0.0267399471969869, 1.50206096236763, 1.00593094545479,
         0.385420876982456, 0.709606530281799, 0.816010051265948, 0.976982348809266, -0.185596354939802,
         0.39115775637264, 0.861606819923965, 0.41844265461532537, -0.0247215106933143, -0.0465897669560321,
         0.084431788275161, -0.250769752776178, 0.382070170178436, 1.01491009313305, -0.138565797433476,
         0.136226382092066, 0.332291831767312, 0.0928391762394073, 0.0711341838396764, 0.0494291914399455,
         0.0277241990402146, -0.00616529872576438, 0.0639684167467785, -0.218433726057223, -0.185943673867669,
         0.0403982236153964, -0.12341633220865, -0.14758486181621833, -0.17175339142378668, -0.195921921031355,
         -0.14108920905524525, -0.0862564970791355, -0.0701966051459052, 0.0804976450381063, -0.237532639332392,
         -0.0692382777572205, 0.0326551923782365, -0.0516831160958379, -0.127233959224877, 0.517080753350909,
         0.303027880999789, 0.227195113407537, 0.593416703489853, 0.412165516605246, 0.124025659777525,
         0.677484123900599, 0.5988407893067135, 0.520197454712828, 0.742048974441803, 0.441286971699162,
         0.921487386069562, 0.589020270856998, 0.4993565059582304, 0.40969274105946274, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         np.nan, np.nan, -2.369883970802335, -2.4595477357011024, -2.54921150059987, 0.361275862229689, 0.359731092245529,
         -0.685975503591877, -0.187823663266091, 1.06338370471753, 0.795156507448635, 1.40686621385683,
         0.528915070165317, 1.70159515966441, 0.255530296191081, 0.0644788117778767, -0.344875529560351,
         0.234232343212298, 0.410422390753063, 0.261706054509793, 0.20144994310775324, 0.14119383170571348, np.nan, np.nan,
         np.nan, np.nan, np.nan, np.nan, np.nan, -0.3408550595106046, -0.40111117091264437, -0.461367282314684, -0.126814125722343,
         0.088997800189515, 0.304809726101373, 0.520621652013231, 0.736433577925089, 0.470526341536136,
         0.4968976605554337, 0.5232689795747315, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
         0.8397248078063044, 0.8660961268256022, 0.8924674458449, -0.531948909319222, 0.599829362193972,
         0.202610151703069, 0.0760801506329743, -0.0292432146045044, -0.764335028494582, -0.242440512878533,
         -0.668890955545244, -0.284907377016267, 0.19085274350426, 0.0342709437222137, -0.766855103871484,
         -0.384087444068199, -0.361216382771729, -0.240665638382411, 0.0799170581197537, 0.271528146563728,
         -0.367019842779011, 0.18322220310272, -0.0233850829919966, 0.310303579033354, 0.206274169899888,
         0.290830615731165, 0.00819931814737466, 0.121006725265371, 0.333438614341769, 0.383705872359046,
         -0.304743120423945, 0.046476836395919, 0.0618770326804435, 0.0586890446961486, -0.0045990870611365,
         0.129349645307683, 0.431358964577807, 0.493116077178144, -0.0196910714810187, 0.0577752725702922,
         0.114042260304346, -0.0371937279670308, 0.101306591063801, 0.0401683636237517, 0.0175262359357439,
         0.125136319994146, 0.0765674853044406, 0.118230039722623, -0.012538821527397, -0.116186318159514,
         -0.243569148560986, -0.00722631974024515, -1.52700911579248, 0.38230000800115, 1.28401164009705,
         0.934589981064783, 0.242514573850979, -0.00226440587939811, 0.0741404800161483, 1.36347948736816,
         1.09436182985553, 0.550105846304484, 0.192165913006511, 0.206339301787148, -0.706414532747557,
         0.272720290769019, 0.19758732674244334, 0.12245436271586765, np.nan, -0.027811565337283684, -0.10294452936385934,
         -0.178077493390435, 0.501903642956598, 1.19911587662748, 0.229284043935278, 0.886873037368612,
         1.17786969408401, -0.129015816164121, -1.13892077409614, 0.0832767245908238, 0.121100995869152,
         0.198041947422979, 0.345475406228199, 0.274529629658162, 0.107798148479268, 0.113788842543583,
         0.119779536607898, 0.125770230672213, 0.131760924736528, 0.137751618800843, 0.16270140218101298,
         0.187651185561183, 0.052169743155109194, -0.0833116992509646, -0.010989600535772692, 0.0613324981794192,
         0.107536216618833, 0.03815546624611, -0.478406571907089, 0.536744495331339, 0.633552736875036,
         0.411096661997775, -0.785378571087788, 0.12167772956152, 0.209438295328186, 1.03082745088076,
         0.150062594143517, -0.561443770894166, 0.210782459887142, 0.27843868332512, -0.15505929281841,
         -0.173994899451575, 0.0180428413849994, 0.015727564176570508, 0.013412286968141611, np.nan, np.nan, np.nan, np.nan]

    y = pd.Series(y)
    x = pd.Series(x)
    df = pd.DataFrame({
        'co2': y,
        'par': x
    })
    a = df.loc[:500]
    b = a.dropna()
    # print(b)
    # p0 = [7, 0.4, 0.1]
    # plsq = optimize.leastsq(residuals, p0, args=(b['co2'], b['par']))
    # print(plsq[0])



    a = df.loc[500:]
    b = a.dropna()
    # print(b)
    p0 = [7, 0.4, 0.1]
    plsq = optimize.leastsq(residuals, p0, args=(b['co2'], b['par']))
    ym = func(b['par'], plsq[0])
    t, p = stats.ttest_ind(b['co2'], ym)
    print(t, p)