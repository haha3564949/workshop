# import tushare as ts
#
# ts.sh_margin_details(start='2015-01-01', end='2015-04-19', symbol='600826')
from  sqlalchemy import create_engine
import tushare as ts
import datetime
import pandas as pd



now=datetime.datetime.now()
engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)
# dfsum=pd.DataFrame(columns=['opDate', 'stockCode', 'securityAbbr', 'rzmre', 'rzye', 'rqmcl', 'rqyl', 'rqye', 'rzrqye'])
dfsum=None;

for i in  range(100):
    delta = datetime.timedelta(days=i+1)
    seachdate=(now-delta).strftime('%Y-%m-%d')

    df=ts.sz_margin_details(date=seachdate)
    if df.size > 0:
        df['rzmre'] = df['rzmre'].astype('string')
        df['rzye']=df['rzye'].astype('string')
        df['rqmcl']=df['rqmcl'].astype('string')
        df['rqyl']=df['rqyl'].astype('string')
        df['rqye']=df['rqye'].astype('string')
        df['rzrqye']=df['rzrqye'].astype('string')
        if i==0:
            dfsum=df
        elif i>0:
            dfsum=dfsum.append(df)
#
# dfa=dfsum.loc[:,['opDate','stockCode','securityAbbr','rzmre','rzye','rqmcl','rqyl','rqye','rzrqye']]


# dfsum.to_sql('sz_margin_details',con=engine, if_exists='replace',chunksize=100,index=True)
dfsum.to_sql('sz_margin_details',con=engine, if_exists='replace',chunksize=100,index=True)
