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



df=ts.sz_margin_details('2018-11-22')
print df

# request = Request(rv.MAR_SZ_HZ_URL % (ct.P_TYPE['http'], ct.DOMAINS['szse'],
#                                       ct.PAGES['szsefc'], date))
\


# request = Request(rv.LHB_SINA_URL_TONY % (ct.P_TYPE['http'], ct.DOMAINS['vsf'],
#
#
#                                     date))

#
# df = pd.read_html(lines, skiprows=[2])[1]
#
# LHB_SINA_URL_TONY = '%s%s/q/go.php/vInvestConsult/kind/rzrq/index.phtml?tradedate=%s'
