import tushare as ts
import datetime
from sqlalchemy import create_engine
# engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)
#
# mydate = datetime.datetime.today()
#
# delta = datetime.timedelta(days=1)
#
# yesterday = datetime.datetime.strptime((mydate - delta).strftime('%Y-%m-%d'),"%Y-%m-%d").weekday()
# print yesterday

# yesterday= (mydate-delta).strptime(mydate-delta, "%Y-%m-%d %H:%M:%S")
# df=ts.sh_margin_details(start='2018-12-25' , end='2018-12-25')
df=ts.get_today_all()

df1 = ts.get_hist_data(code='600030', start='2018-12-24', end='2018-12-31')
# df4 = ts.sh_margin_details(symbol=scode, start='2017-01-01', end='2018-10-31')
print df1


http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(tdate=%272019-01-07%27)