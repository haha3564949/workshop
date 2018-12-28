#-*-coding:utf-8-*-
import tushare as ts
import talib as tb
import pandas as pd
from  sqlalchemy import create_engine
import datetime
from sqlalchemy.dialects.oracle import   DATE,FLOAT,  NUMBER,   VARCHAR2

engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)

# engine = create_engine('oracle://test:test@192.168.24.131/orcl',echo=True)
def getInitWebData(startnum,endnum):
    mydate = datetime.datetime.today()
    for i in range(startnum,endnum+1):
        delta = datetime.timedelta(days=i)
        tempday = (mydate - delta).strftime('%Y-%m-%d')
        df=ts.sz_margin_details(date=tempday,retry_count=3,pause=0.01)
        if len(df)>0:
            df1=df.iloc[:,[1,2,3,7,10,11]]
            df1['rqye']=df1['rqye'].replace('--', '-1');
            df1['opDate'] = pd.to_datetime(df1['opDate'], format='%Y-%m-%d %H:%M:%S')
            df1.to_sql('rzrqtemp', con=engine, if_exists='append', chunksize=100, index=False,dtype={'stockCode':VARCHAR2(20),'securityAbbr':VARCHAR2(20),'rqye':FLOAT,'rzye':FLOAT});
            print i
def getInitPriceData(startnum,endnum):
    mydate = datetime.datetime.today()
    startdelta = datetime.timedelta(days=startnum)
    enddelta = datetime.timedelta(days=endnum)
    enddate = (mydate - startdelta).strftime('%Y-%m-%d')
    startdate = (mydate - enddelta).strftime('%Y-%m-%d')
    print startdate,enddate
    df=pd.read_sql("select distinct rq.\"stockCode\" from rzrqtemp rq",engine);
    for i in df['stockCode']:
        df_price=ts.get_hist_data(code=i, start=startdate , end=enddate)
        df_price=df_price.reset_index();
        df_price=df_price.loc[:,['close','date']]
        df_price['date'] = pd.to_datetime(df_price['date'], format='%Y-%m-%d %H:%M:%S')
        df_price['stockCode']=i
        df_price.to_sql('rzrqprice',con=engine, if_exists='append', chunksize=100, index=False,dtype={'stockCode':VARCHAR2(6)} )

def updateInitWebData(sql):
    try:
        pd.read_sql(sql,engine);
    except Exception, e:
        print e.message

def getDBData():

    df1 = pd.read_sql(
        """ select distinct  a."stockCode"  from szrzrq a  """,
        engine)
    dftemp = pd.DataFrame(columns=['stockCode', 'securityAbbr', 'rzrqye', 'opDate', 'ema', 'emas', 'emaq', 'diff', 'dea', 'macd'])
    for str in df1.iloc[:,0]:
        df2 = pd.read_sql(
            """select  a.* from szrzrq a where dbms_lob.substr(a."stockCode")=:a  order by dbms_lob.substr(a."opDate")  asc""",
            engine, params={"a": str})
        df3=calc_MACD(df2)
        dftemp=dftemp.append(df3)

    dftemp.to_sql('myszrzrq', con=engine, if_exists='append', chunksize=100, index=False)


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

def main():
    # every day before 9:00 AM ,else the trade should be exchanged to settlement
    startnum=1
    endnum=2
    getInitWebData(startnum, endnum);
    getInitPriceData(startnum, endnum);
    # updateInitWebData("merge into rzrqtemp rzt "
    #                   " using rzrqprice rzp  on (rzt.\"stockCode\" = rzp.\"stockCode\" and rzt.\"opDate\" = rzp.\"date\"  and  rzt.rzye<0  "
    #                   "        ) "
    #                   "   when matched then "
    #                   " update set rzt.rqye = rzt.rzye+rzt.rqyl*(rzp.close) ");




if __name__ == '__main__':
    main()
   #get history rzrqdata
# getDBData()     #calculate the rzrqye data