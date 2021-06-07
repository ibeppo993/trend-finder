#(VALORE - MIN) / (MAX - MIN) * 100
#https://github.com/nithinmurali/pygsheets
import pygsheets, os, gspread
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


json_authentication_file = os.environ.get("json_authentication_file")
python_customer_metrics_1 = os.environ.get("python_customer_metrics_1")
path = 'output_data/'
current_file = f'{path}12_zz_finish.csv'


#creazione dataframe
df = pd.read_csv(current_file, sep='\t', encoding='UTF-8')
#print(df.info())
print(df)

#Selezione ultimo anno di olonne
min_v = 1
max_v = 200
list_week = []
for c_week in range(min_v,max_v):
    list_week.append(c_week)
#print(list_week)
df.drop(df.columns[list_week], axis = 1, inplace = True)
#print(df.info())
print(df)

#Creazione lista con nome colonne
columns_name = df.columns.tolist()
print(columns_name)
columns_name.remove('Week')
print(columns_name)

value_list = marks_list = df['Week'].tolist()
print(value_list)

for value_name in value_list:
    new_row = df.loc[(df[value_name])]
    print(new_row)



'''
for index, row in df.iterrows():
    print(row)
'''
'''
list_n = [0,1,2,3,4,5,6,7,8,9,10]

value_min = min(list_n)
print(value_min)

value_max = max(list_n)
print(value_max)

print('-------------')
new_list = []

for value in list_n:
    new_min = value - value_min
    max_min = value_max - value_min
    result = (new_min / max_min) *100
    print(result)
    new_list.append(result)

print(list_n)
print(new_list)
'''


