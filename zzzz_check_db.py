import sqlite3, time, os
import pandas as pd
from z_ads_prepare import create_db_ads
from dotenv import load_dotenv

load_dotenv()
create_db_ads()



def select_keyword():
    conn = sqlite3.connect(db_name_keyword)
    c = conn.cursor()
    global keywords_list_db
    keywords_list_db = []
    for x in range(0, n_keywords):
        data = pd.read_sql_query("SELECT KEYWORDS FROM KEYWORDS_LIST WHERE SUM <> 2 AND CHECKING = 0 LIMIT 1;", conn)
        #print(type(data['KEYWORDS'].iat[0]))
        keyword = (data['KEYWORDS'].iat[0])
        keywords_list_db.append(keyword)
        c.execute("Update KEYWORDS_LIST set CHECKING = 1 where KEYWORDS = ?", (keyword,))
    conn.commit()
    conn.close()
    #print(keywords_list_db)



def check_record_db():
    conn = sqlite3.connect(db_name_keyword)
    c = conn.cursor()
    data = pd.read_sql_query("SELECT KEYWORDS FROM KEYWORDS_LIST WHERE SUM <> 2 AND CHECKING = 0 ;", conn)
    global numbers_kw
    numbers_kw = len(data)
    print(numbers_kw)
    conn.commit()
    conn.close()

    

db_name_keyword = os.environ.get("db_name_keyword_ads")

n_keywords = 5



check_record_db()
if numbers_kw < n_keywords:
    n_keywords = 1

select_keyword()

