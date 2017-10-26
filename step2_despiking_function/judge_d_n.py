# 1 is daytime, 0 is nighttime  according to PAR
class JudgeDN:
    def judge_dn(self, data, threshold):
        return data


class PAR(JudgeDN):
    def judge_dn(self, data, threshold):
        data.loc[data['PAR_dn_Avg'] > threshold, 'daytime'] = 1
        data.loc[data['PAR_dn_Avg'] <= threshold, 'daytime'] = 0
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
    # judge_dn = {}
    # judge_dn[1] = DNContext(PAR)
    # judge_dn[2] = DNContext(SLR)
    # ctype = input("type:[1]for PAR,[2]for SLR")
    # if ctype in judge_dn:
    #     cc = judge_dn[ctype]
    # else:
    #     print("Undefine type. Use PAR mode.")
    #     cc = judge_dn[1]
    # print("you will pay:%d" % (cc.GetResult(data, threshold)))