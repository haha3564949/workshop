#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime

engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)

def getWebData():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    today = (today - delta).strftime('%Y-%m-%d')
    stock_info=ts.get_stock_basics()
    for i in stock_info.index:
        if i.startswith('6'):
            df1 = ts.get_hist_data(code='600523',start=today,end=today)
            df4 = ts.sh_margin_details(symbol='600523',start=today, end=today)
            if len(df4)>0:
                df4=df4.set_index('opDate')
                df5=pd.merge(df1,df4,how='left',left_index=True,right_index=True)
                df5=df5.loc[:,['open','high','low','close','volume','rzye','rqyl']]
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

                dffinal.to_sql('myrzrqye', con=engine, if_exists='append', chunksize=100, index=True)
        # df.to_csv("test.csv")


def getDBData():
    # result = engine.execute('select * from myrzrqye')
    # print(result.fetchall())
    df2=pd.read_sql('select a.* from myrzrqye a where a."index"=?',engine,params={9})
    print df2


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
# getWebData()
#
# df4 = ts.sh_margin_details(symbol=600856,start='2018-08-01', end='2018-09-18')
# print df4
getDBData()