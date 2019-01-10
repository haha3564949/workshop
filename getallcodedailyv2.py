#-*-coding:utf-8-*-
import tushare as ts
from tushare.stock import cons as ct
import urllib
import pandas as pd
import json
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

from  sqlalchemy import create_engine
import datetime
# from sqlalchemy.dialects.oracle import   DATE,FLOAT,  NUMBER,   VARCHAR2
from sqlalchemy.dialects.mysql import   DATE,FLOAT,   VARCHAR

# engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)
engine=create_engine('mysql+mysqldb://root:123@192.168.11.129:3306/rzrq?charset=utf8')
# engine = create_engine('oracle://test:test@192.168.11.129/orcl',echo=True)
def getInitWebData(startnum,endnum):
    mydate = datetime.datetime.today()
    for i in range(startnum,endnum+1):
        delta = datetime.timedelta(days=i)
        tempday = (mydate - delta).strftime('%Y-%m-%d')
        try:
            url = ct.EASTMONEY_TONY % (ct.P_TYPE['http'], ct.DOMAINS['em1'], '\''+tempday+'\'')
            request = Request(url)
            lines = urlopen(request, timeout=10).read()
            df = pd.read_json(lines, orient='record', dtype={"scode": str })
            dftable=df.loc[:,['rzrqye','scode','sname','tdate']]
            dftable.to_sql('rzrqtemp', con=engine, if_exists='append', chunksize=100, index=False,dtype={'scode':VARCHAR(20),'sname':VARCHAR(20),'rzrqye':FLOAT,'tdate':DATE});

            # df=ts.sz_margin_details(date=tempday,retry_count=3,pause=0.01)
            # if len(df)>0:
            #     df1=df.iloc[:,[1,2,3,7,10,11]]
            #     df1['rqye']=df1['rqye'].replace('--', '-1');
            #     df1['opDate'] = pd.to_datetime(df1['opDate'], format='%Y-%m-%d %H:%M:%S')
            #     df1.to_sql('rzrqtemp', con=engine, if_exists='append', chunksize=100, index=False,dtype={'stockCode':VARCHAR(20),'securityAbbr':VARCHAR(20),'rqye':FLOAT,'rzye':FLOAT});
            #     print i
        except Exception,e:
            print("Error:",e)
            print tempday
def getInitPriceData(startnum,endnum):
    mydate = datetime.datetime.today()
    startdelta = datetime.timedelta(days=startnum)
    enddelta = datetime.timedelta(days=endnum)
    enddate = (mydate - startdelta).strftime('%Y-%m-%d')
    startdate = (mydate - enddelta).strftime('%Y-%m-%d')
    print startdate,enddate
    # df=pd.read_sql("select distinct rq.stockCode from rzrqtemp rq",engine);
    # for i in df['stockCode']:
    #     df_price=ts.get_hist_data(code=i, start=startdate , end=enddate)
    #     df_price=df_price.reset_index();
    #     df_price=df_price.loc[:,['close','date']]
    #     df_price['date'] = pd.to_datetime(df_price['date'], format='%Y-%m-%d %H:%M:%S')
    #     df_price['stockCode']=i
    #     df_price.to_sql('rzrqprice',con=engine, if_exists='append', chunksize=100, index=False,dtype={'stockCode':VARCHAR(6)} )

def updateInitWebData(sql):
    try:
        pd.read_sql(sql,engine);
    except Exception, e:
        print e.message


def getDBData():

    df1 = pd.read_sql(
        " select distinct  a.scode  from rzrqtemp a where a.rzrqye is not null" ,
        engine)
    dftemp = pd.DataFrame(columns=['scode', 'sname', 'rzrqye', 'tdate', 'ema', 'emas', 'emaq', 'diff', 'dea', 'macd'])
    for str in df1.iloc[:,0]:
        sql="select * from (select  a.* from rzrqall a where a.scode=%s and a.rzrqye is not null order by a.tdate desc limit 27)aa  union  select '' as 'dea','' as 'diff' ,'' as  'ema','' as 'emaq','' as 'emas' ,'' as 'macd',rzrqye,scode,sname,tdate from rzrqtemp  where scode=%s and tdate>(select  max(a.tdate) from rzrqall a where a.scode=%s) order by 10 desc"
        sql1=sql % (str,str,str)
        df2 = pd.read_sql(sql1
            ,
            engine)
        df3=calc_MACD(df2)
        # df3 = df3.loc[[26]]
        dftemp=dftemp.append(df3)
        print str
    dftemp.to_sql('rzrqall', con=engine, if_exists='append', chunksize=100, index=False,dtype={'stockCode':VARCHAR(6),'securityAbbr':VARCHAR(20)} )


def calc_EMA(df, N):
    # for i in range(len(df)):
        # if i==0:
        #     df.ix[i,'ema']=int(df.ix[i,'rzrqye'])
        # if i>0:
    ema = ((N - 1) * (float(df.ix[1, 'ema'])) + 2 * float(df.ix[0, 'rzrqye'])) / (N + 1)
    df.ix[0, 'ema'] = ema
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
    df.ix[0,'dea'] = ((M-1)*float((df.ix[1,'dea'])) + 2*float(df.ix[0,'diff']))/(M+1)
    df.ix[0,'macd'] = 2*(float(df.ix[0,'diff'])- float(df.ix[0,'dea']))
    return df.loc[[0]]

def main():
    # every day before 9:00 AM ,else the trade should be exchanged to settlement
    startnum=1
    endnum=1
    getInitWebData(startnum, endnum);
    # getInitPriceData(startnum, endnum);
    # updateInitWebData("update rzrqtemp rzt set rzt.rqye = rzt.rzye+rzt.rqyl*(select rzp.close from rzrqprice rzp where rzt.stockCode = rzp.stockCode and rzt.opDate= rzp.date) "
    #                   "    where  rzt.rqye<0 ");
    getDBData()



if __name__ == '__main__':
    main()
   #get history rzrqdata
# getDBData()     #calculate the rzrqye data