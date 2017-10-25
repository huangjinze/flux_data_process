# 1 is daytime, 0 is nighttime  according to PAR
def judge_DN_PAR(data):
    data.loc[data.PAR_dn_Avg > 5, 'daytime'] = 1
    data.loc[data.PAR_dn_Avg <= 5, 'daytime'] = 0
    return data

def judge_DN_SLR(data):
    data.loc[data.Slr_Avg > 5, 'daytime'] = 1
    data.loc[data.Slr_Avg <= 5, 'daytime'] = 0
    return data

if __name__ == '__main__':
    pass