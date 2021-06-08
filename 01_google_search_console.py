import pickle
import pandas as pd
import time
import os 

from datetime import datetime, timedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build

from dotenv import load_dotenv
load_dotenv()

print('primo')

timestr = time.strftime("%Y%m%d-%H%M%S")
SITE_URL = os.environ.get("GSC_SITE_URL")
print(SITE_URL)
print(timestr)
# There are only two OAuth Scopes for the Google Search Console API
# For the most part, all you will need is `.readonly` but if you want to modify data in Google Search Console,
# you will need the second scope listed below
# Read more: https://developers.google.com/webmaster-tools/search-console-api-original/v3/
OAUTH_SCOPE = ('https://www.googleapis.com/auth/webmasters.readonly', 'https://www.googleapis.com/auth/webmasters')

# Redirect URI for installed apps
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

# This is auth flow walks you through the Web auth flow the first time you run the script and stores the credentials in a file
# Every subsequent time you run the script, the script will use the "pickled" credentials stored in config/credentials.pickle
try:
 credentials = pickle.load(open("config_file/credentials.pickle", "rb"))
except (OSError, IOError) as e:
    flow = InstalledAppFlow.from_client_secrets_file("config_file/client_secret_555711575796-j821ki3bi9glb8tnp787i4r08b1od81i.apps.googleusercontent.com.json", scopes=OAUTH_SCOPE)
    credentials = flow.run_console()
    pickle.dump(credentials, open("config_file/credentials.pickle", "wb"))

# Connect to Search Console Service using the credentials
webmasters_service = build('webmasters', 'v3', credentials=credentials)

maxRows = 25000
i = 0

output_rows = []
#date a mano
#start_date = datetime.strptime("2020-01-15", "%Y-%m-%d")
#end_date = datetime.strptime("2020-01-16", "%Y-%m-%d")s

#date automatiche
#per spezzare l'anno in 4
# 370 - 277
# 276 - 183
# 182 - 89
# 88 - 1

start_date = datetime.now() + timedelta(days=-10)
end_date = datetime.now() + timedelta(days=-3)

#print(start_date)
#print(end_date)

def date_range(start_date, end_date, delta=timedelta(days=1)):
    """
    The range is inclusive, so both start_date and end_date will be returned
    Args:
        start_date: The datetime object representing the first day in the range.
        end_date: The datetime object representing the second day in the range.
        delta: A datetime.timedelta instance, specifying the step interval. Defaults to one day.
    Yields:
        Each datetime object in the range.
    """
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += delta

for date in date_range(start_date, end_date):
    date = date.strftime("%Y-%m-%d")
    print(date)
    print('pausa 25 secondi')
    time.sleep(25)
    i = 0
    while True:

        request = {
            'startDate' : date,
            'endDate' : date,
            'dimensions' : ["query","page","country","device"],
            "searchType": "Web",
            'rowLimit' : maxRows,
            'startRow' : i * maxRows
        }

        response = webmasters_service.searchanalytics().query(siteUrl = SITE_URL, body=request).execute()
        print()
        if response is None:
            print("there is no response")
            break
        if 'rows' not in response:
            print("row not in response")
            break
        else:
            for row in response['rows']:
                keyword = row['keys'][0]
                page = row['keys'][1]
                country = row['keys'][2]
                device = row['keys'][3]
                output_row = [date, keyword, page, country, device, row['clicks'], row['impressions'], row['ctr'], row['position']]
                output_rows.append(output_row)
            i = i + 1

# Salva il file con la data nel nome
#root = 'output'
#df = pd.DataFrame(output_rows, columns=['date','query','page', 'country', 'device', 'clicks', 'impressions', 'ctr', 'avg_position'])
#df.to_csv(root + '/' + f"{timestr}-gsc.csv")

# Salva il file senza data nel nome
root = 'output_data/'

if not os.path.exists(root):
    os.makedirs(root)


df = pd.DataFrame(output_rows, columns=['date','query','page', 'country', 'device', 'clicks', 'impressions', 'ctr', 'avg_position'])
df.to_csv(root +f'01_google_search_console.csv', index=False, sep = ';')

# passaggio al secondo file
#os.system('python3 2_google_search_console.py')