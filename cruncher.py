import subprocess as subp
import subprocess
import time, os, datetime
import psutil


#Get a list of all processes with a certain name
def get_pid(name):
    return list(map(int,subp.check_output(["pidof", "-c", name]).split()))

max_num_processi = 1
pausa_1 = 1
pausa_2 = 1
pausa_3 = 1
file_da_eseguire = 'scrape_serp_selenium.py'

a = 1
i = 0
print("al mio segnale scatenate i processi :D")
time.sleep(pausa_1)


#Avvio primo terminale
os.system(f"<gnome-terminal -x python3 {file_da_eseguire}")

while a == 1:
    #Get a list of all pids for python3 processes
    python_pids = get_pid('python3')
    #Get a list of all pids for processes with "main.py" argument
    try:
        main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", f"{file_da_eseguire}"]).split()))
    except subprocess.CalledProcessError as e:
        print('nessun processo attivo')
        os.system(f"gnome-terminal -x python3 {file_da_eseguire}")
        print('YYYYYYYY-----processo eseguito')
        time.sleep(pausa_1)
        main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", f"{file_da_eseguire}"]).split()))

    
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
    else:
        print('XXXXXXX----raggiunto il numero massimo di processi')
        time.sleep(pausa_3)
    
    '''
    os.system("killall --quiet --older-than 1w python3")

    python_pids = get_pid('python3')
    main_py_pids = list(map(int,subp.check_output(["pgrep", "-f", f"{file_da_eseguire}"]).split()))
    python_main_py_pid = set(python_pids).intersection(main_py_pids)
    print(main_py_pids)
    try:
        for pid in main_py_pids:
            p = psutil.Process(pid)
            asdasd = p.create_time
            print(asdasd)
    except err:
        print('pid già eliminato')
        #date_creation_pid = datetime.datetime.fromtimestamp(p.create_time).strftime("%Y-%m-%d %H:%M")
        #print(date_creation_pid)
    '''

    print('-----------------------FINITO')


