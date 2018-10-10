#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime
# import logging
# logger=logging.getLogger()
# logger.setLevel(logging.INFO)

# engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)

engine = create_engine('oracle://test:test@192.168.24.131/orcl',echo=True)
def getData(yesterday):
    tempday=yesterday
    df=ts.sz_margin_details(date=tempday,retry_count=3,pause=0.01)
    if len(df)>0:
        df1=df.iloc[:,[0,1,7,8]]
        # df1['opDate'] = df1['opDate'].astype('string')
        # df1['securityAbbr'] = df1['securityAbbr'].astype('string')
        df1['rzrqye'] = df1['rzrqye'].astype('string')
        # df1['stockCode'] = df1['stockCode'].astype('string')
        dftemp = pd.DataFrame(
            columns=['stockCode', 'securityAbbr', 'rzrqye', 'opDate', 'ema', 'emas', 'emaq', 'diff', 'dea', 'macd'])
        dftemp=dftemp.append(df1)
        dftemp.to_sql('myszrzrq', con=engine, if_exists='append', chunksize=100, index=False)

def getDBData(yesterday):
    tempday=yesterday
    df1 = pd.read_sql(
        """select  distinct dbms_lob.substr(a."stockCode") from szrzrq a  """,
        engine)
    dftemp = pd.DataFrame(columns=['stockCode', 'securityAbbr', 'rzrqye', 'opDate', 'ema', 'emas', 'emaq', 'diff', 'dea', 'macd'])
    for str in df1.iloc[:,0]:
        df2 = pd.read_sql(
            """select * from (select  a.* from myszrzrq a where dbms_lob.substr(a."stockCode")=:a  order by dbms_lob.substr(a."opDate")  desc)A where rownum<3 """,
            engine, params={"a": str})
        df3=calc_MACD(df2)
        dftemp=dftemp.append(df3)
    conn = engine.connect()
    try:
        sql = 'delete from myszrzrq a where dbms_lob.substr(a."opDate")=\'%s\' and a.Macd is null' % tempday
        conn.execute(sql)
    except Exception as ee:
        print ee
        # logger.error("fileToMysql fialed",ee)
        # traceback.print_exc()

    finally:
        conn.close()

    dftemp.to_sql('myszrzrq', con=engine, if_exists='append', chunksize=100, index=False)


def calc_EMA(df, N):
    # for i in range(len(df)):
        # if i==0:
        #     df.ix[i,'ema']=df.ix[i,'rzrqye']
        # if i>0:
    ema=((N-1)*(float(df.ix[1,'ema']))+2*float(df.ix[0,'rzrqye']))/(N+1)
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
    df.ix[0,'dea'] = ((M-1)*(df.ix[1,'dea']) + 2*float(df.ix[0,'diff']))/(M+1)
    df.ix[0,'macd'] = 2*(float(df.ix[0,'diff'])- float(df.ix[0,'dea']))
    return df.loc[[0]]

def main():
    mydate = datetime.datetime.today()
    delta = datetime.timedelta(days=1)
    yesterday = (mydate - delta).strftime('%Y-%m-%d')
    getData(yesterday)
    getDBData(yesterday)

if __name__ == '__main__':
    main()