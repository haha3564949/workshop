#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine


engine = create_engine('oracle://test:test@192.168.24.131/orcl',echo=True)


def getData():
    stock_info=ts.get_stock_basics()
    for i in stock_info.index:
        if i.startswith('6'):
            df1 = ts.get_hist_data(code=i,start='2018-08-01',end='2018-09-18')
            df4 = ts.sh_margin_details(symbol=i,start='2018-08-01', end='2018-09-18')
            if len(df4)>0:
                df4=df4.set_index('opDate')
                df5=pd.merge(df1,df4,how='left',left_index=True,right_index=True)
                df5=df5.loc[:,['open','high','low','close','volume','rzye','rqyl','stockCode']]
                df5['rzrqye']=df5['rqyl']*df5['close']+df5['rzye']
                df=df5.sort_index()
                # calc_MACD(df, 12, 26, 9).to_csv("d:\\workshop\\workshop\\ab\\"+i+".csv")
                dffinal=calc_MACD(df, 12, 26, 9)
                dffinal=dffinal.reset_index()
                dffinal['date'] = dffinal['date'].astype('string')
                dffinal['open'] = dffinal['open'].astype('string')
                dffinal['high'] = dffinal['high'].astype('string')
                dffinal['low'] = dffinal['low'].astype('string')
                dffinal['close'] = dffinal['close'].astype('string')
                dffinal['volume'] = dffinal['volume'].astype('string')
                dffinal['rzye'] = dffinal['rzye'].astype('string')
                dffinal['rqyl'] = dffinal['rqyl'].astype('string')
                dffinal['rzrqye'] = dffinal['rzrqye'].astype('string')
                dffinal['ema'] = dffinal['ema'].astype('string')
                dffinal['diff'] = dffinal['diff'].astype('string')
                dffinal['dea'] = dffinal['dea'].astype('string')
                dffinal['macd'] = dffinal['macd'].astype('string')
                dffinal['stockCode'] = dffinal['stockCode'].astype('string')
                dffinal.to_sql('myrzrqye', con=engine, if_exists='append', chunksize=100, index=True)
        # df.to_csv("test.csv")
#
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
    df['diff']=list(temp)
    for i in range(len(df)):
       if i==0:
           df.ix[i,'dea'] = df.ix[i,'diff']
       if i>0:
            df.ix[i,'dea'] = ((M-1)*df.ix[i-1,'dea'] + 2*df.ix[i,'diff'])/(M+1)
    df['macd'] = 2*(df['diff']- df['dea'])
    return df
getData()
#
# df4 = ts.sh_margin_details(symbol=600856,start='2018-08-01', end='2018-09-18')
# print df4