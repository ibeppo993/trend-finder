import subprocess as subp
import time, os, datetime, subprocess, psutil, sqlite3
import pandas as pd
from z_trends_prepare import create_db_and_folder
from dotenv import load_dotenv
load_dotenv()

create_db_and_folder()
db_name_keyword = os.environ.get("db_name_keyword")

def check_record_db():
    conn = sqlite3.connect(db_name_keyword)
    c = conn.cursor()
    data = pd.read_sql_query("SELECT KEYWORDS FROM KEYWORDS_LIST WHERE SUM <> 2 AND CHECKING = 0 ;", conn)
    global numbers_kw
    numbers_kw = len(data)
    print(numbers_kw)
    conn.commit()
    conn.close()

#Get a list of all processes with a certain name
def get_pid(name):
    return list(map(int,subp.check_output(["pidof", "-c", name]).split()))

max_num_processi = 1
pausa_1 = 1
pausa_2 = 1
pausa_3 = 1
file_da_eseguire = '05_google_trends_2.py'

a = 1
i = 0
print("al mio segnale scatenate i processi :D")
time.sleep(pausa_1)


#Avvio primo terminale
os.system(f"<gnome-terminal -x python3 {file_da_eseguire}")

check_record_db()
while numbers_kw != 0:
    #Get a list of all pids for python3 processes
    python_pids = get_pid('python3')
    #Get a list of all pids for processes with "main.py" argument
    try:
        main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", f"{file_da_eseguire}"]).split()))
        check_record_db()
    except subprocess.CalledProcessError as e:
        print('nessun processo attivo')
        os.system(f"gnome-terminal -x python3 {file_da_eseguire}")
        print('YYYYYYYY-----processo eseguito')
        time.sleep(pausa_1)
        main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", f"{file_da_eseguire}"]).split()))
        check_record_db()

    
    #main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", f"{file_da_eseguire}"]).split()))
    python_main_py_pid = set(python_pids).intersection(main_py_pids)
    #print(python_pids)
    print(main_py_pids)
    #print(python_main_py_pid)
    number_of_python_process = len(main_py_pids)
    print(number_of_python_process)

    time.sleep(pausa_1)

    if number_of_python_process < max_num_processi:
        os.system(f"gnome-terminal -x python3 {file_da_eseguire}")
        print('YYYYYYYY-----processo eseguito')
        time.sleep(pausa_1)
        check_record_db()
    else:
        print('XXXXXXX----raggiunto il numero massimo di processi')
        time.sleep(pausa_3)
        check_record_db()


    print('-----------------------FINITO')


