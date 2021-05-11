import pytrends
from pytrends.request import TrendReq
import pandas as pd
import time
import datetime
from datetime import date
import csv, os
from pytrends import *
from dotenv import load_dotenv
load_dotenv()

file_kw = os.environ.get("file_kw_trend")
output_files = os.environ.get("output_files_trend")
file_name = os.environ.get("file_name_trend")
file_proxies = os.environ.get("file_proxies_trend")
timestr = time.strftime('%Y%m%d-%H%M%S')

#
#
#Trend di ricerche nel tempo
#
#

#creazione lista da file txt
# with open('kw1-1.txt') as file:
#     searches  = [searches .rstrip('\n') for searches  in file]
# print(searches)

f = open(file_kw, 'r', encoding='utf8', errors='ignore')
searches= f.read().split('\n')

if not os.path.exists(output_files):
    os.makedirs(output_files)

#with proxies
with open(file_proxies , encoding='utf-8') as f:
    proxies = [line.rstrip() for line in f]

#pytrend =TrendReq(hl='it-IT', tz=360, timeout=(10,25), proxies=proxies, retries=10, backoff_factor=0.1)#, requests_args={'verify':False})

# without proxy
pytrend = TrendReq(hl='it-IT', tz=360)

groupkeywords = list(zip(*[iter(searches)]*1))
#print(groupkeywords)
groupkeywords = [list(x) for x in groupkeywords]
#print(groupkeywords)

dicti = {}
i = 1

sec_wait_time=1
pri_wait_time=6

numyears=5
numdays = 7
numweeks = 52
total_time_range = numdays * numweeks * numyears
end_date= date.today()
today_date = date.today()
end_date = today_date
begin_date = end_date - datetime.timedelta(days = total_time_range-7)
user_timeframe = begin_date.strftime('%Y-%m-%d')+' '+end_date.strftime('%Y-%m-%d')

def run_chunk(frm,to):
	global dicti
	global i
	for ind in range(frm,to):
		try:
			trending=groupkeywords[ind]
			print(i," : ",trending)
			pytrend.build_payload(trending,timeframe=user_timeframe , geo = 'IT')
			dicti[i] = pytrend.interest_over_time()
			# print( dicti[i] )
		except:
			print("--------------")
			pass
		i+=1
		time.sleep(sec_wait_time)
		print("Delay : ",sec_wait_time," s")


length = len(groupkeywords)
l_limit=0
limit_gap=5
r_limit=l_limit+limit_gap

if r_limit>length:
	r_limit=length

cnt = 0
while r_limit<=length:
	run_chunk(l_limit,r_limit)
	cnt+=limit_gap
	if r_limit>=length:
		break
	l_limit=r_limit
	if r_limit+limit_gap<=length:
		r_limit+=limit_gap
	else:
		r_limit=length

	if dicti!={}:
		result = pd.concat(dicti, axis=1)
		result.columns = result.columns.droplevel(0)
		if 'isPartial'in result.columns:
			result = result.drop('isPartial', axis = 1)
		result.to_csv(f'{output_files}/{file_name}', sep=';')
		#pd.read_csv(f'{output_files}/{timestr}-3-gtrends.csv', header=None, sep=';').T.to_csv(f'{output_files}/{timestr}-3-gtrends.csv', header=False, index=False, sep=';')
		time.sleep(pri_wait_time )
		print("Delay : ",pri_wait_time," s")
	if cnt>100:
		cnt=0
		print("Delay Starting for 1min: ")
		time.sleep(1*60)
		print("Delay Starting for 1min: ")

#Transposizione righe con colonne
