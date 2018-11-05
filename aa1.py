import tushare as ts
import datetime
from sqlalchemy import create_engine
engine = create_engine('oracle://tony:tony@192.168.137.131/orcl',echo=True)

mydate = datetime.datetime.today()

delta = datetime.timedelta(days=1)

yesterday = datetime.datetime.strptime((mydate - delta).strftime('%Y-%m-%d'),"%Y-%m-%d").weekday()
print yesterday

# yesterday= (mydate-delta).strptime(mydate-delta, "%Y-%m-%d %H:%M:%S")
