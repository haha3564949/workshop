import tushare as ts

df1 = ts.get_hist_data(code="600826", start='2017-01-01', end='2018-09-25')



# df4 = ts.sh_margin_details(symbol=scode, start='2017-01-01', end='2018-09-25')

print df1