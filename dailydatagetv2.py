#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime


engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)

# engine = create_engine('oracle://test:test@192.168.24.131/orcl',echo=True)
def getDBData():
    # result = engine.execute('select * from myrzrqye')
    # print(result.fetchall())
    df2=pd.read_sql("""select  dbms_lob.substr(a."date")  "date",dbms_lob.substr(a."stockCode") "stockCode",dbms_lob.substr(a.close) "close",dbms_lob.substr(a.rzrqye) "rzrqye",dbms_lob.substr(a.emas) "emas",dbms_lob.substr(a.emaq) "emaq",dbms_lob.substr(a.diff) "diff",dbms_lob.substr(a.dea) "dea",dbms_lob.substr(a.macd) "macd" from myrzrqye a  """,engine)

    return df2


def getWebData(yesterday):

    df = ts.get_today_all();
    df1 =df.loc[:,['code','settlement']];
    df1.rename(columns={'settlement': 'close','code':'stockCode'},inplace=True);
    df2 = ts.sh_margin_details(start=yesterday, end=yesterday)
    dfresult= pd.DataFrame(
            columns=['date', 'close', 'dea', 'diff', 'emaq', 'emas', 'macd', 'rzrqye', 'stockCode', 'ema'])

    if len(df2)>0 and len(df1)>0 :
        df2=df2.set_index('stockCode');
        df1=df1.set_index('stockCode');
        df3=pd.merge(df1,df2,how='left',left_index=True,right_index=True)
        df3=df3.loc[:,['close','rqyl','rzye','opDate']]
        df3['rzrqye']=df3['rqyl']*df3['close']+df3['rzye']

        df4 = getDBData()
        df4 = df4.set_index('stockCode');
        for scode in filter(isSHStock,df3.index):
            print scode
            df6=df4.filter(regex=scode,axis=0)
            df6=df6.sort_values(by='date',ascending=False)
            if(len(df6)>27):
                df6=df6.iloc[0:27,]
            if(len(df6)>0):
                df6=df6.reset_index();
                df6.rename(columns={'index': 'stockCode'}, inplace=True);
                df6=df6.set_index("date")
                df5=df3.filter(regex=scode,axis=0);
                df5=df5.reset_index('stockCode');
                df5=df5.set_index('opDate')
                df5=df5.loc[:,['close','rzrqye','stockCode']]
                df=df5.append(df6);
                dffinal = calc_MACD(df, 12, 26, 9)
                dffinal = dffinal.reset_index()

                dffinal.rename(columns={'index': 'date'},inplace=True);
                dffinal = dffinal.loc[[0]]
                dfresult=dfresult.append(dffinal)
        dfresult.to_sql('myrzrqye', con=engine, if_exists='append', chunksize=100, index=False)


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


def main():
    mydate = datetime.datetime.today()
    delta= datetime.timedelta(days=1)
    if mydate.weekday() ==0:
        delta = datetime.timedelta(days=3)
    if mydate.weekday() == 6:
        delta = datetime.timedelta(days=2)

    yesterday = (mydate - delta).strftime('%Y-%m-%d')

    getWebData(yesterday)

if __name__ == '__main__':
    main()