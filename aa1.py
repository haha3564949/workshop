import tushare as ts
import datetime
from sqlalchemy import create_engine
engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)
#
# mydate = datetime.datetime.today()
# delta = datetime.timedelta(days=1)
# yesterday = (mydate - delta).strftime('%Y-%m-%d')
#
#
# #
# conn = engine.connect()
# try:
#     sql = 'delete from myszrzrq a where dbms_lob.substr(a."opDate")=\'%s\' and a.Macd is null' % yesterday
#     # print sql
#     conn.execute(sql)
# except Exception as ee:
#     print  ee
# #
# #     # logger.error("fileToMysql fialed",ee)
# #     # traceback.print_exc()
# #
# # finally:
# #     conn.close()

df=ts.get_today_all();
df1 = df.loc[:, ['code', 'settlement']];
print df1
# df4 = ts.sh_margin_details(start='2018-10-30', end='2018-10-30')

# ['code', 'symbol', 'name', 'changepercent','trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio',  'amount', 'per', 'pb', 'mktcap', 'nmc']

# df.to_sql('testdata',con=engine, if_exists='append',chunksize=100,index=True)