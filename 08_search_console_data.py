import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

file_kw = os.environ.get("csv_kw_file")
dataframe = pd.read_csv(file_kw, encoding='utf-8', sep='\t', header=None, low_memory=False)
dataframe = dataframe.iloc[:, 0]
dataframe = dataframe.to_frame().reset_index(drop=True)
dataframe = dataframe.iloc[1:]
print(dataframe)

first_column = dataframe.iloc[:, 0]
list_kw = first_column.tolist()
#print(list_kw)



file_gsc = 'output_data/02_google_search_console.csv'
df = pd.read_csv(file_gsc, encoding='utf-8', sep=';', low_memory=False)
print(df)
new_df = df[df['query'].isin(list_kw)]
new_df = new_df.drop(['date','page'], 1)
print(new_df)

new_df.to_csv('output_data/12_search_console_data.csv', index=False, sep='\t', decimal=',')