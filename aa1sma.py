from  sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import talib
import numpy as np
import cx_Oracle


conn = cx_Oracle.connect("tony/tony@192.168.137.131:1521/orcl")
cursor = conn.cursor ()

sql ="select dbms_lob.substr(a.\"stockCode\") as stockCode,dbms_lob.substr(a.\"securityAbbr\") as securityAbbr,dbms_lob.substr(a.\"opDate\") as opDate,dbms_lob.substr(a.\"RZRQYE\") as RZRQYE  from sz_margin_details  a where dbms_lob.substr(a.\"stockCode\")=000001  order by 3 desc"
cursor.execute(sql)
rows = cursor.fetchall()
data = pd.DataFrame(rows,columns=['stockCode','securityAbbr','opDate','RZRQYE'])


securityAbbr = data.loc[:,'securityAbbr']
securityAbbr = pd.Series([item.decode('GBK').encode('UTF-8') for item in securityAbbr])
data.loc[:,'securityAbbr'] = securityAbbr
# print data
ma=data.loc[:,'RZRQYE']


data['macd'], data['macdsignal'], data['macdhist'] = talib.MACD(ma, fastperiod=12, slowperiod=26, signalperiod=9)
data.to_csv("aa.csv")



