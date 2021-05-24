# https://facebook.github.io/prophet/docs/quick_start.html
import pandas as pd
from prophet import Prophet

from matplotlib import pyplot as plt
from matplotlib.dates import MonthLocator, num2date
from matplotlib.ticker import FuncFormatter
import os, time, sqlite3

from dotenv import load_dotenv
load_dotenv()

db_name_keyword = os.environ.get("db_name_keyword_prophet")

if os.path.isfile('output_data/10_trend_forecast.csv'):
    os.remove('output_data/10_trend_forecast.csv')
else:
    print ("File not exist")

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

# creazione dataframe da file csv + transposizione 
df = pd.read_csv('output_data/09_zz_finish.csv', sep='\t')


#creazione lista kw da dataframe
kw_list = df['date'].tolist()
#print(kw_list)

df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df = df.T
df = df.rename(columns=df.iloc[0])
df = df.iloc[1:]
df.dropna()
#print(df)

for keyword in kw_list:
    # lavorazione dataframe
    print(keyword)

    # selezione colonna da predire e conversione index in data
    df_kw = df[[f'{keyword}']]
    df_kw.reset_index(inplace=True)
    df_kw.columns = ['ds', 'y']
    df_kw['ds'] = pd.to_datetime(df_kw['ds'], errors='coerce')
    #print(df)

    # # rimozione NaN
    # for value in df['ds']:
    #     print(value)

    # inizio previsione
    m = Prophet(weekly_seasonality=True)
    m.fit(df_kw)

    future = m.make_future_dataframe(periods=8, freq='W')
    future.tail()

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(forecast)
    #print(type(forecast))

    df_toprint = forecast[['ds', 'yhat']]
    #print(df_toprint)

    fig1 = m.plot(forecast)
    # plt.show()

    timestr = time.strftime('%Y%m%d-%H')
    if os.path.isfile('output_data/10_trend_forecast.csv'):
        #print('##########################################################file exist1')
        df_toprint.columns = ['week', f'{keyword}']
        #df_toprint.set_index('week')
        #print(df_toprint.info())

        #print('##########################################################file exist2')
        df_to_concat = pd.read_csv(f'output_data/10_trend_forecast_{timestr}.csv', sep='\t', decimal=",")#, index_col='week')
        #df_to_concat.set_index('week')
        df_to_concat['week'] = pd.to_datetime(df_to_concat['week'])
        #print(df_to_concat.info())
        #print(df_to_concat)

        #result = pd.concat([df_to_concat, df_toprint], axis=1, )
        result = pd.DataFrame.merge(df_toprint,df_to_concat,on='week')
        #print(result)
        result.to_csv(f'output_data/10_trend_forecast_{timestr}.csv', sep='\t', index=False, decimal=",")

    else:
        #print ("File not exist")
        df_toprint.columns = ['week', f'{keyword}']
        df_toprint.set_index('week')
        df_toprint.to_csv(f'output_data/10_trend_forecast_{timestr}.csv', sep='\t', index=False, decimal=",")


#df_to_transpone = pd.read_csv(f'output_data/10_trend_forecast_{timestr}.csv', sep='\t')#, decimal=",")
#print(df_to_transpone)
#df_to_transpone2 = df_to_transpone.T
#print(df_to_transpone2)
#df_to_transpone2.to_csv('output_data/10_2_trend_forecast.csv', sep='\t',header=False, decimal=",")

