# 1 is daytime, 0 is nighttime  according to PAR
class JudgeDN:
    def judge_dn(self, data, threshold):
        return data


class PAR(JudgeDN):
    def judge_dn(self, data, threshold):
        data.loc[data['PAR_net_Avg'] > threshold, 'daytime'] = 1
        data.loc[data['PAR_net_Avg'] <= threshold, 'daytime'] = 0
        return data


class SLR(JudgeDN):
    def judge_dn(self, data, threshold):
        data.loc[data['Slr_Avg'] > threshold, 'daytime'] = 1
        data.loc[data['Slr_Avg'] <= threshold, 'daytime'] = 0
        return data


class DNContext:
    def __init__(self, method):
        self.method = method

    def get_method(self, data, threshold):
        return self.method.judge_dn(data, threshold)

if __name__ == '__main__':
    pass
