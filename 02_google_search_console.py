import pandas as pd
import os, time, subprocess


print('secondo')

root = 'output_data/'
root_kw = 'input_data/'

if not os.path.exists(root_kw):
    os.makedirs(root_kw)

#condition = df.a < 10
#df.where(cond=condition,inplace=True)

'''
df2 = pd.read_csv('output/gsc.csv', usecols = ['query','impressions'])
df2.sort_values(by=["impressions"], ascending=False)
#df2[df2["impression"] == '1.0'
df2.drop_duplicates(subset ="query", keep = False, inplace = True) 
df2.to_csv(root + '/' + 'gsc2.csv')

# passaggio al terzo file
os.system('python third.py')
'''
#brand = 'vanoli'

df2 = pd.read_csv(root +'01_google_search_console.csv', usecols = ['query','impressions','clicks','page','date','country','avg_position'],sep = ';')
df2['sumimppression'] = df2.groupby(['query','page'])['impressions'].transform('sum')
del df2['impressions']
df2['sumclicks'] = df2.groupby(['query','page'])['clicks'].transform('sum')
del df2['clicks']
df2 = df2[df2.country == 'ita']
df2 = df2.drop(columns=['country'])
colonne = list(df2)
print(colonne)
df2 = df2.sort_values(['query', 'date',],ascending=[False, False])
count_duplicate_query = df2.pivot_table(index=['query'], aggfunc='size')
print(count_duplicate_query)
df2.drop_duplicates(subset ="query", keep = 'first', inplace = True)
df2.sort_values("sumimppression", inplace = True, ascending = False)

#Left_join = pd.merge(df2, count_duplicate_query, on ='query',how ='right') 
#print(Left_join)

'''
df2.sort_values('date').drop_duplicates('query',keep='last')
df2.drop_duplicates(subset ="query", keep = 'first', inplace = True)
print(df2)
'''
#Rimozione numero di impression basso
df3 = df2[df2.sumimppression > 22]
#print(df3)



df3.to_csv(root+'02_google_search_console.csv', index=False, sep = ';')
print(df3.head())
#selection = df3.loc['query']
#print(selection)

selection = df3['query']
print(selection)
selection.to_csv(root_kw+'keywords.txt', index=False,header=False)
