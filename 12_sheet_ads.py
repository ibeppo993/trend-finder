#https://github.com/nithinmurali/pygsheets
import pygsheets, os, gspread
import numpy as np
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


json_authentication_file = os.environ.get("json_authentication_file")
python_customer_metrics_1 = os.environ.get("python_customer_metrics_1")
path = 'output_data/'
current_file = f'{path}6_google_ads_export-Volume.csv'


#
#
# CURRENT FILE
#
#
#creazione dataframe
cols_to_use = [0,1,3,4]
df = pd.read_csv(current_file,usecols=cols_to_use, sep='\t', encoding='UTF-8')
#print(df.info())
#conteggio righe df
numbers_of_rows = len(df)
#print(numbers_of_rows)
row_sheet = numbers_of_rows +1
print(row_sheet)
#conteggio colonne df
numbers_of_columns = len(df.columns)
column_sheet = numbers_of_columns
#print(column_sheet)

#apertura Google Sheet
gc = pygsheets.authorize(service_file=json_authentication_file)
# Open spreadsheet and then worksheet
sh = gc.open_by_key(python_customer_metrics_1)
wks = sh.worksheet_by_title('row_ads_data')

#Creazione riche da csv ecommerce
rows = row_sheet
wks.rows=rows
cols = column_sheet
wks.cols=cols #colonna O
wks.clear()

#scrittura con rige dataframe
df_row = pd.read_csv (current_file, sep='\t',usecols=cols_to_use, encoding='UTF-8', header=None, low_memory=False)
#print(df_row.info())
df_row = df_row.replace(np.nan, 0)

total_rows = row_sheet -1
print(total_rows)
total_rows = total_rows // 2000
print(total_rows)

splitted_dataframe = np.array_split(df_row, total_rows)
#print(splitted_dataframe)
#print(type(splitted_dataframe))
# for little_dataframe in splitted_dataframe:
#     numbers_of_rows_ld = len(little_dataframe)
#     print(numbers_of_rows_ld)

for little_dataframe in splitted_dataframe:
    cell_list = wks.range('A:A')

    i = 1
    for cell in cell_list:
        #print(cell)
        #print(len(cell_list))
        cell_str = str(cell)
        #print(type(cell))
        in_list = "''" in cell_str
        #print(in_list)
        if in_list == False:
            i += 1

    wks.insert_rows(row=i, number=1)

    little_dataframe.columns = little_dataframe.iloc[0]
    little_dataframe = little_dataframe[1:]
    #print(little_dataframe)

    #little_dataframe = numpy.delete(little_dataframe, index)
    print(i)
    wks.set_dataframe(little_dataframe,(i, 1))
