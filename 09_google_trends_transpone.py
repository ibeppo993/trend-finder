import glob, os, time
import pandas as pd
from os import listdir
from dotenv import load_dotenv
from os import listdir

load_dotenv()

output_files = os.environ.get("output_files_trend")
file_name = os.environ.get("file_name_trend")
file_name_transpone = os.environ.get("file_name_transpone_trend")
timestr = time.strftime('%Y%m%d-%H%M%S')
timestr = time.strftime('%Y%m%d-%H%M%S')
file_trends = f'{output_files}/{file_name}'
file_trends_t = f'{output_files}/{file_name_transpone}'


#os.chdir(os.environ.get("output_files_trend"))
file_list = []
for file in glob.glob(f'{output_files}/08_google*.csv'):
    #print(file)
    #print('-----')
    file_list.append(file)
#print('-----------print list')
print(file_list)


i = 0
for trend_file in file_list:
    print(trend_file)
    #print(f'{trend_file}')
    #print(f'{trend_file}_transpone')
    #df_toprint2 = pd.read_csv(f'{trend_file}', sep='\t')
    #print(df_toprint2)
    print('---------------------------------------------------------')
    pd.read_csv(f'{trend_file}', header=None, sep='\t', low_memory=False).T.to_csv(f'{output_files}/09_gtrends_transpone_{i}.csv', header=False, index=False, sep='\t')
    i += 1


files = glob.glob('output_data/09_gtrends_transpone*.csv')
#print(files)
dfs = [pd.read_csv(f, header=None, sep="\t") for f in files]

trans_df = pd.concat(dfs,ignore_index=True)
date_filter = 'date'
print(trans_df.info())
print(trans_df)

#print(trans_df.at[0,0])
trans_df.at[0,0] = 'Week'
#print(trans_df.at[0,0])


trans_df = trans_df[trans_df[0] != date_filter]
new_header = trans_df.iloc[0] #grab the first row for the header
trans_df = trans_df[1:] #take the data less the header row
trans_df.columns = new_header #set the header row as the df header


trans_df = trans_df.drop_duplicates(subset='Week', keep="first").dropna(axis='columns')
print(trans_df)

#min = 1
#max = 104
#list_week = []
#for c_week in range(min,max):
#    list_week.append(c_week)
#print(list_week)
#trans_df.drop(trans_df.columns[list_week], axis = 1, inplace = True)
#print(trans_df.info())

#trans_df.to_csv('output_data/09_zz_finish.csv', sep='\t', index=False, header=False)
trans_df.to_csv('output_data/09_zz_finish.csv', sep='\t', index=False)


files_to_remove = glob.glob('output_data/09_gtrends_transpone*.csv')
#print(files_to_remove)
for file_r in files_to_remove:
    os.remove(file_r)
