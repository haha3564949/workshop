#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime




engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)
def getDBData(str):
    # result = engine.execute('select * from myrzrqye')
    # print(result.fetchall())
    df2=pd.read_sql("""select * from (select  a.* from myrzrqye a where dbms_lob.substr(a."stockCode")=:a  order by dbms_lob.substr(a."date")  desc)A where rownum<27 """,engine,params={"a":str})

    return df2


def getWebData():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    today = (today - delta).strftime('%Y-%m-%d')
    stock_info=ts.get_stock_basics()

    b = []
    for i in stock_info.index:
        if i.startswith("6"):
            b.append(i)

    stock_info = stock_info.loc[b]
    stock_info = stock_info.sort_index()
    total = len(stock_info)
    i = 0

    for scode in stock_info.index:
        i = i + 1
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", i, "/", total
        if scode.startswith('6'):
            df1 = ts.get_hist_data(code=scode,start=today,end=today)
            df4 = ts.sh_margin_details(symbol=scode,start=today, end=today)


            # df1 = ts.get_hist_data(code='601012',start=today,end=today)
            # df4 = ts.sh_margin_details(symbol='601012',start=today, end=today)

            if len(df4)>0 and len(df1)>0 :
                df4=df4.set_index('opDate')
                df5=pd.merge(df1,df4,how='left',left_index=True,right_index=True)
                df5=df5.loc[:,['open','high','low','close','volume','rzye','rqyl','stockCode']]
                df5['rzrqye']=df5['rqyl']*df5['close']+df5['rzye']
                df2=getDBData(scode)
                if len(df2)>0:
                # df2 = getDBData(scode)
                    df2=df2.set_index("date")
                    df=df5.append(df2)
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
                    dffinal=dffinal.loc[[0]]
                    dffinal.to_sql('myrzrqye', con=engine, if_exists='append', chunksize=100, index=False)
        # df.to_csv("test.csv")




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
getWebData()
