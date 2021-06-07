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
#print(df)

#Selezione ultimo anno di colonne
min_v = 1
max_v = 200
list_week = []
for c_week in range(min_v,max_v):
    list_week.append(c_week)
#print(list_week)
df.drop(df.columns[list_week], axis = 1, inplace = True)
df_float = df.copy()
#print(df_float.info())
#print(df_float)

#per ogni riga
for index in df_float.index:
    print(index)

    # lista dei valori per riga
    list_value = []

    for column in df_float.columns:
        #print(column)
        predict_value = df_float.loc[index,column]
        #print(predict_value)
        if type(predict_value) == str:
            predict_value = predict_value.replace(',','.')
        #print(predict_value)
        #print(type(predict_value))
        list_value.append(predict_value)
    name = list_value[0]
    print(name)
    
    del list_value[0]
    #print(list_value)

    list_of_floats = []
    for item in list_value:
        #item_float = item.replace(',','.')
        list_of_floats.append(float(item))
    
    #print(list_of_floats)


    #
    #
    #Da 0 a 100
    value_min_0_100 = min(list_of_floats)
    #print(value_min_0_100)

    value_max_0_100 = max(list_of_floats)
    #print(value_max_0_100)

    #print('-------------')
    new_list = []

    for value in list_of_floats:
        new_min = value - value_min_0_100
        max_min = value_max_0_100 - value_min_0_100
        result = (new_min / max_min) *100
        #print(result)
        new_list.append(result)

    #print(list_of_floats)
    #print(new_list)

    #
    #
    #

    new_list.insert(0,name)


    #print(df_float)
    df_float.drop(df_float[df_float['Week'] == name].index, inplace=True)
    

    col_list = list(df_float)


    dictionary_list = zip(col_list, new_list)
    a_dictionary = dict(dictionary_list)
    #print(a_dictionary)
    df_to_append = pd.DataFrame([a_dictionary])
    #print(df_to_append)


    #df_to_append = df_to_append.T
    #print(df_to_append)
    df_float = df_float.append(df_to_append)

print(df_float)


