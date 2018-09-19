#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd


# d = {'one' : pd.Series([1, 2, 3], index=['a', 'b', 'c']),
#     'two' : pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])}
#
# df = pd.DataFrame(d)
# print df
#
#
# df1=pd.DataFrame([{'rzche': 111864384L, 'securityAbbr': u'\u6d1b\u9633\u94bc\u4e1a', 'rqmcl': 564700L, 'opDate': u'2018-08-28', 'rqyl': 1868400L, 'rzye': 2130516160L, 'rqchl': 256200L, 'stockCode': u'603993', 'rzmre': 113198250L, u'"index"': 5510L}, {'rzche': 66038011L, 'securityAbbr': u'\u6d1b\u9633\u94bc\u4e1a', 'rqmcl': 151200L, 'opDate': u'2018-08-27', 'rqyl': 1559900L, 'rzye': 2129182294L, 'rqchl': 94400L, 'stockCode': u'603993', 'rzmre': 85196955L, u'"index"': 5511L}])
# print df1.iloc[:,0].size

import pandas as pd

df1 = ts.get_hist_data('600826',start='2017-01-01',end='2018-09-14')

df4=ts.sh_margin_details(symbol='600826',start='2017-01-01',end='2018-09-14')
df4=df4.set_index('opDate')


df5=pd.merge(df1,df4,how='left',left_index=True,right_index=True)

df5=df5.loc[:,['open','high','low','close','volume','rzye','rqyl']]
df5['rzrqye']=df5['rqyl']*df5['close']+df5['rzye']

df=df5.sort_index()

def calc_EMA(df, N):
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=df.ix[i,'rzrqye']
        if i>0:
            df.ix[i,'ema']=((N-1)*df.ix[i-1,'ema']+2*df.ix[i,'rzrqye'])/(N+1)
    ema=list(df['ema'])
    return ema

def calc_MACD(df, short=12, long=26, M=9):
    emas = calc_EMA(df, short)
    emaq = calc_EMA(df, long)
    temp = pd.Series(emas) - pd.Series(emaq)
    df['diff']=temp
    for i in range(len(df)):
       if i==0:
           df.ix[i,'dea'] = df.ix[i,'diff']
       if i>0:
            df.ix[i,'dea'] = ((M-1)*df.ix[i-1,'dea'] + 2*df.ix[i,'diff'])/(M+1)
    df['macd'] = 2*(df['diff'] - df['dea'])
    return df
calc_MACD(df, 12, 26, 9).to_csv("ab.csv")