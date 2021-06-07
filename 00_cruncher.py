import subprocess as subp
import subprocess
import time, os, datetime
import psutil

def file_1():
    file = '01_google_search_console.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_2():
    file = '02_google_search_console.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_3():
    # file = '04_trend_manager.py'
    # time.sleep(5)
    # file1 = '04_trend_manager_1.py'
    # time.sleep(5)
    # file2 = '04_trend_manager_2.py'

    # cmd = subprocess.Popen(['python3',f"{file}"])
    # time.sleep(5)
    # cmd = subprocess.Popen(['python3',f"{file1}"])
    # time.sleep(5)
    # cmd = subprocess.Popen(['python3',f"{file2}"])
    # time.sleep(5)
    # cmd.communicate()
    file = '03_trends_cruncher.py'
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_4():
    file = '06_google_trends_transpone.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_5():
    file = '07_google_ads_keywords_volume.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_6():
    file = '08_search_console_data.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_7():
    file = '09_prophet_prediction.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_8():
    file = '10_prophet_prediction_transpone.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

def file_8_1():
    file = '11_prophet_prediction_0_100.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()


def file_9():
    file = '12_sheet_ads.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()
    time.sleep(5)

def file_10():
    file = '12_sheet_search_console.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()
    time.sleep(5)

def file_11():
    file = '12_sheet_trends_detail.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()
    time.sleep(5)

def file_12():
    file = '12_sheet_trends_general.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()
    time.sleep(5)

def file_13():
    file = '12_sheet_prediction_detail.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()
    time.sleep(5)

def file_14():
    file = '12_sheet_prediction_general.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()
    time.sleep(5)
    
def file_15():
    file = '13_clean_folder.py'
    print(f'{file}')
    cmd = subprocess.Popen(['python3',f"{file}"])
    cmd.communicate()

file_1()
file_2()
file_3()
file_4()
file_5()
file_6()
file_7()
file_8()
file_8_1()
file_9()
file_10()
file_11()
file_12()
file_13()
file_14()
#file_15()

