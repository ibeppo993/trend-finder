import pytrends, io, sqlite3, urllib, time, datetime, csv, os, random
from pytrends.request import TrendReq
import pandas as pd
from datetime import date
from datetime import datetime
from pytrends import *
from trends_prepare import create_db_and_folder
from dotenv import load_dotenv
load_dotenv()

create_db_and_folder()

file_kw = os.environ.get("file_kw_trend")
output_files = os.environ.get("output_files_trend")
file_name = os.environ.get("file_name_trend")
file_proxies = os.environ.get("file_proxies")
db_name_keyword = os.environ.get("db_name_keyword")
db_name_proxy = os.environ.get("db_name_proxy")

timestr = time.strftime('%Y%m%d-%H%M%S')


def select_proxy():
    conn = sqlite3.connect(db_name_proxy)
    c = conn.cursor()
    data = pd.read_sql_query(
        "SELECT PROXY FROM PROXY_LIST WHERE TIME = ( SELECT MIN(TIME) FROM PROXY_LIST);", conn)
    # print(type(data['PROXY'].iat[0]))
    global proxy
    proxy = (data['PROXY'].iat[0])
    print(f'---------------------Request IP is {proxy}')
    timestr_now = str(datetime.now())
    # print(timestr_now)
    # global timestr
    timestr = datetime.fromisoformat(timestr_now).timestamp()
    # print(timestr)
    c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?", (timestr, proxy))
    conn.commit()
    c.execute("Update PROXY_LIST set TIME = ? where PROXY = ?",
              (timestr, proxy,))
    conn.commit()
    # print('pausa 1 sec')
    conn.close()


def select_keyword():
    print('-------------------------')
    conn = sqlite3.connect(db_name_keyword)
    c = conn.cursor()
    data = pd.read_sql_query(
        "SELECT KEYWORDS FROM KEYWORDS_LIST WHERE SUM <> 2 AND CHECKING = 0 LIMIT 1;", conn)
    # print(type(data['KEYWORDS'].iat[0]))
    global keyword
    keyword = (data['KEYWORDS'].iat[0])
    c.execute("Update KEYWORDS_LIST set CHECKING = 1 where KEYWORDS = ?", (keyword,))
    conn.commit()
    conn.close()
    # print(new_keyword)


#
#
# Trend di ricerche nel tempo
#
#
while True:
	select_keyword()
	select_proxy()

	print(f'keyword ------- {keyword}')
	single_search=keyword
	dataset = []

	proxies = []
	proxies.append(proxy)
	print(proxies)

	kw_list = []
	kw_list.append(keyword)
	print(kw_list)
	# print(keyword)
	# pytrend = TrendReq(hl='it-IT', tz=360)
	pytrend =TrendReq(hl='it-IT', tz=360, timeout=(10,25), proxies=proxies, retries=10, backoff_factor=0.1)#, requests_args={'verify':False})
	pytrend.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='IT-IT', gprop='')
	data = pytrend.interest_over_time()
	# print(data)
	if not data.empty:
		# data.drop(labels=['isPartial'], axis='columns')
		data = data.drop(labels=['isPartial'],axis='columns')
		dataset.append(data)

	try:
		result = pd.concat(dataset, axis=1)
		# print(result.info())
		# print(result)

		timestr = time.strftime('%Y%m%d-%H')
		if os.path.isfile(f'output_data/08_google_trends_{timestr}.csv'):
			df_file = pd.read_csv(f'output_data/08_google_trends_{timestr}.csv', sep='\t', index_col='date')
			# print(df_file)
			# print(df_file.info())
			df_file.index = df_file.index.astype(str)
			df_file.index = df_file.index.str.replace(' 00:00:00', '')
			# new_result = pd.concat([df_file,result], axis=1)
			result.index = result.index.astype(str)
			result.index = result.index.str.replace(' 00:00:00', '')
			
			new_result = pd.concat([df_file,result], axis=1)
			# print(new_result.info())
			new_result.to_csv(f'output_data/08_google_trends_{timestr}.csv', sep='\t')
			print('--------------DataFrame concatenato')


		else:
			result.to_csv(f'output_data/08_google_trends_{timestr}.csv', sep='\t')
			print('--------------DataFrame scritto')
	except:
		print('--------------DataFrame VUOTO')
