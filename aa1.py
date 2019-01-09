import tushare as ts
from tushare.stock import cons as ct
import urllib
import pandas as pd
import json
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

import datetime

url = ct.EASTMONEY_TONY % (ct.P_TYPE['http'], ct.DOMAINS['em1'] , '\'2019-01-07\'')
request = Request(url)
lines = urlopen(request, timeout=10).read()
df=pd.read_json(lines,orient='record',dtype={"scode":str,"tdate":datetime})

print df

# EASTMONEY_TONY='%s%s/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(tdate=%s)'

# 'em1':'dcfm.eastmoney.com'}


# http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=RZRQ_DETAIL_NJ&token=70f12f2f4f091e459a279469fe49eca5&filter=(tdate=%272019-01-07%27)