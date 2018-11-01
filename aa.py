# import tushare as ts
#
# ts.sh_margin_details(start='2015-01-01', end='2015-04-19', symbol='600826')
from  sqlalchemy import create_engine
import tushare as ts

# df=ts.sh_margins(start='2018-08-01', end='2018-08-19')
engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)
# # df.rename(columns={'opDate':'opdate'}, inplace = True)
# # df.to_sql('tick_data3',con=engine, if_exists='fail')
# df.to_sql('tick_data',con=engine, if_exists='replace')


df=ts.sh_margin_details(start='2016-01-01', end='2016-12-31')
df['rzye']=df['rzye'].astype('string')
df['rzmre']=df['rzmre'].astype('string')
df['rzche']=df['rzche'].astype('string')
df['rqyl']=df['rqyl'].astype('string')
df['rqmcl']=df['rqmcl'].astype('string')
df['rqchl']=df['rqchl'].astype('string')
df.to_sql('sh_margin_details',con=engine, if_exists='append',chunksize=100,index=True)
