import os, time, sqlite3, random
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from os import path
from dotenv import load_dotenv
load_dotenv()

def create_db_and_folder():
    output_html = os.environ.get("output_trends")
    teporary_file = os.environ.get("teporary_file")
    input_data = os.environ.get("input_data")
    file_kw = input_data+os.environ.get("kw_file")


    #creazione Cartelle
    config_file = 'config_file'
    if not os.path.exists(output_html):
        os.makedirs(output_html)
    # if not os.path.exists(output_screenshot):
    #     os.makedirs(output_screenshot)
    if not os.path.exists(teporary_file):
        os.makedirs(teporary_file)
    test_proxy = 'output_html/test_proxy.txt'


    #
    #
    # File
    #file_kw = input_data+'/keywords.txt'
    file_proxies = os.environ.get("file_proxies")
    db_name_keyword = os.environ.get("db_name_keyword")
    db_name_proxy = os.environ.get("db_name_proxy")


    #
    #
    # Creazione dataframe proxy
    dataframe = pd.read_csv(file_proxies, encoding='utf-8', header=None)
    #timestr = time.strftime('%Y-%m-%d %H:%M:%S')
    timestr_now = str(datetime.now())
    #print(timestr_now)
    timestr = datetime.fromisoformat(timestr_now).timestamp()
    #print(timestr)
    dataframe['TIME'] = timestr
    dataframe.columns = ['PROXY','TIME']
    #print(dataframe)


    #
    #
    # Creazione DB da Dataframe PROXY
    check_db = path.exists(db_name_proxy)
    #print(check_db)
    if check_db == False:
        conn = sqlite3.connect(db_name_proxy,detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        c.execute('CREATE TABLE PROXY_LIST (PROXY text, TIME timestamp)')
        conn.commit()
        df = DataFrame(dataframe, columns= ['PROXY','TIME'])
        df.to_sql('PROXY_LIST', conn, if_exists='replace', index = True)
        c.execute('''  
        SELECT * FROM PROXY_LIST
                ''')
        # for row in c.fetchall():
        #     print(row)
        del df
        del dataframe
        conn.close()
    else:
        print('DB già presente PROXY')


    #
    #
    # Creazione dataframe keyword
    dataframe = pd.read_csv(file_kw, encoding='utf-8', sep=';', header=None)
    dataframe['CHECKING'] = 0
    dataframe['SUM'] = 0
    dataframe.columns = ['KEYWORDS','CHECKING','SUM']
    #print(dataframe)


    #
    #
    # Creazione DB da Dataframe KEYWORD
    check_db = path.exists(db_name_keyword)
    #print(check_db)
    if check_db == False:
        conn = sqlite3.connect(db_name_keyword)
        c = conn.cursor()
        c.execute('CREATE TABLE KEYWORDS_LIST (KEYWORDS text, CHECKING number, SUM number)')
        conn.commit()
        df = DataFrame(dataframe, columns= ['KEYWORDS', 'CHECKING', 'SUM'])
        df.to_sql('KEYWORDS_LIST', conn, if_exists='replace', index = True)
        c.execute('''  
        SELECT * FROM KEYWORDS_LIST
                ''')
        #for row in c.fetchall():
        #    print(row)
        del df
        del dataframe
        conn.close()
    else:
        print('DB già presente KEYWORDS')


#create_db_and_folder()