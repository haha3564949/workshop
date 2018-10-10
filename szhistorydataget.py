#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime

# engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)

engine = create_engine('oracle://test:test@192.168.24.131/orcl',echo=True)
def getData():
    mydate = datetime.datetime.today()
    for i in range(1,646):
        delta = datetime.timedelta(days=i)
        tempday = (mydate - delta).strftime('%Y-%m-%d')
        df=ts.sz_margin_details(date=tempday,retry_count=3,pause=0.01)
        if len(df)>0:
            df1=df.iloc[:,[0,1,7,8]]
            # df1['opDate'] = df1['opDate'].astype('string')
            # df1['securityAbbr'] = df1['securityAbbr'].astype('string')
            df1['rzrqye'] = df1['rzrqye'].astype('string')
            # df1['stockCode'] = df1['stockCode'].astype('string')
            df1.to_sql('szrzrq', con=engine, if_exists='append', chunksize=100, index=False)
            print i
def getDBData():
    df1 = pd.read_sql(
        """  """,
        engine)
    for str in df1.iloc[:,0]:
        df2 = pd.read_sql(
            """select  a.* from szrzrq a where dbms_lob.substr(a."stockCode")=:a  order by dbms_lob.substr(a."opDate")  asc""",
            engine, params={"a": str})
        df3=calc_MACD(df2)
        df3.to_sql('myszrzrq', con=engine, if_exists='append', chunksize=100, index=False)


def calc_EMA(df, N):
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=int(df.ix[i,'rzrqye'])
        if i>0:
            df.ix[i,'ema']=((N-1)*int(df.ix[i-1,'ema'])+2*int(df.ix[i,'rzrqye']))/(N+1)
    ema=list(df['ema'])
    return ema

def calc_MACD(df, short=12, long=26, M=9):
    emas = calc_EMA(df, short)
    df['emas']=list(emas)
    emaq = calc_EMA(df, long)
    df['emaq']=list(emaq)
    temp = pd.Series(emas) - pd.Series(emaq)
    df['diff']=list(temp)
    for i in range(len(df)):
       if i==0:
           df.ix[i,'dea'] = df.ix[i,'diff']
       if i>0:
            df.ix[i,'dea'] = ((M-1)*df.ix[i-1,'dea'] + 2*df.ix[i,'diff'])/(M+1)
    df['macd'] = 2*(df['diff']- df['dea'])
    return df
# getData()
getDBData()