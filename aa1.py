import tushare as ts

# df=ts.sh_margin_details(symbol="600826",start="2018-09-25",end="2018-09-25")
# df2=ts.get_h_data(start='2018-09-25',end='2018-09-25')
df1 = ts.get_hist_data( code="600826",start="2018-09-25",end="2018-09-25")
# df1 = ts.sh_margin_details(start="2018-09-25",end="2018-09-25") #ok without code
#
# print df1


