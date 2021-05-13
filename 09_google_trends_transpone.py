import pandas as pd
import time, os
from dotenv import load_dotenv
load_dotenv()


output_files = os.environ.get("output_files_trend")
file_name = os.environ.get("file_name_trend")
file_name_transpone = os.environ.get("file_name_transpone_trend")
timestr = time.strftime('%Y%m%d-%H%M%S')



timestr = time.strftime('%Y%m%d-%H%M%S')
file_trends = f'{output_files}/{file_name}'
file_trends_t = f'{output_files}/{file_name_transpone}'

pd.read_csv(file_trends, header=None, sep='\t', low_memory=False).T.to_csv(file_trends_t, header=False, index=False, sep='\t')
