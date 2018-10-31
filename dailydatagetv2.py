#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime




engine = create_engine('oracle://test:test@192.168.24.131/orcl',echo=True)
def getDBData(str):
    # result = engine.execute('select * from myrzrqye')
    # print(result.fetchall())
    df2=pd.read_sql("""select * from (select  a.* from myrzrqye a where dbms_lob.substr(a."stockCode")=:a  order by dbms_lob.substr(a."date")  desc)A where rownum<27 """,engine,params={"a":str})

    return df2


def getWebData():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=4)
    today = (today - delta).strftime('%Y-%m-%d')
    df = ts.get_today_all();
    df1 =df.loc[:,['code','settlement']];
    df4 = ts.sh_margin_details(start='2018-10-30', end='2018-10-30')



    if len(df4)>0 and len(df1)>0 :
        df4=df4.set_index('stockCode');
        df1=df1.set_index('code');
        df5=pd.merge(df1,df4,how='left',left_index=True,right_index=True)
        df5=df5.loc[:,['settlement','rqyl','rzye','start']]
        df5['rzrqye']=df5['rqyl']*df5['settlement']+df5['rzye']
        for scode in filter(isSHStock,df5.index):
            print scode
            df2=getDBData(scode)
            df2=df2.set_index("date")
            df6=df5.filter(regex=scode,axis=0);





def calc_EMA(df, N):
    # for i in range(len(df)):
        # if i==0:
        #     df.ix[i,'ema']=df.ix[i,'rzrqye']
        # if i>0:
    ema=((N-1)*(float(df.ix[1,'ema']))+2*df.ix[0,'rzrqye'])/(N+1)
    df.ix[0,'ema']=ema
    return ema

def calc_MACD(df, short=12, long=26, M=9):
    df['ema']=df['emas']
    emas = calc_EMA(df, short)
    df.ix[0,'emas']=emas
    df['ema']=df['emaq']
    emaq = calc_EMA(df, long)
    df.ix[0,'emaq']=emaq
    temp = emas - emaq
    df.ix[0,'diff']=temp
    df.ix[0,'dea'] = ((M-1)*float(df.ix[1,'dea']) + 2*df.ix[0,'diff'])/(M+1)
    df.ix[0,'macd'] = 2*(df.ix[0,'diff']- df.ix[0,'dea'])
    return df
def isSHStock(str):
    return str.startswith('6');

getWebData()
