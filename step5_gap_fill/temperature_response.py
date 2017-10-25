import numpy as np
from scipy import optimize


if __name__ == '__main__':
    # def func(x, p):
    #     A, k, theta = p
    #     return A*np.sin(2*np.pi*k*x+theta)
    # def residuals(p, y, x):
    #     return y-func(x, p)
    #
    # x=np.linspace(0, 2*np.pi, 100)
    # A, k, theta = 10, 0.34, np.pi/6
    # y0 = func(x, [A, k, theta])
    # np.random.seed(0)
    # y1 = y0+2*np.random.randn(len(x))
    #
    # p0 = [7, 0.40, 0]
    #
    # plsq = optimize.leastsq(residuals, p0, args=(y1, x))
    # plsq1 = np.linalg.lstsq(y1, x)
    #
    # print([A, k, theta])
    # print(plsq)
    # print(plsq1)

    import matplotlib.pyplot as plt
    from scipy import stats
    x = np.linspace(-5, 5, 500)
    print(np.mean(x))
    print(np.var(x))
    print(stats.ttest_1samp(x, 1))