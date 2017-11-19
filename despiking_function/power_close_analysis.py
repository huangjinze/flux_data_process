
import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri
from rpy2.robjects.packages import importr
pandas2ri.activate()
base = importr('base')
stats = importr('stats')

def funcR():
    '''
    H + LE = b1 + b2 * (Rn - G_mean)
    :param x: =Rn=,=G_mean=
    :param p: =H=,=LE=
    :return: <string>
    '''
    return 'H + LE ~b1 + b2 * (Rn_Avg - G_mean)'

def PCA_method(data):
    '''
    calculate gradient of power close analysis
    :param data: <dataframe>data set including =LE=,=H=,=Rn_Avg=,=G=
    :return: the gradient and intercept
    '''
    robjects.globalenv['df'] = data
    A = stats.nls(
        funcR(),
        data=base.as_symbol('df')
    )
    intercept = base.summary(A).rx2('coefficients')[0]
    gradient = base.summary(A).rx2('coefficients')[1]
    return intercept, gradient

if __name__ == '__main__':
    import init_data.opt_database as optdb

    db = optdb.DB()
    data = db.db_read_data('2012_yc_1_despiking')
    PCA_method(data)
