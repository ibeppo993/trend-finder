#https://groups.google.com/g/adwords-api/c/LbeNND7ovKY
#https://developers.google.com/adwords/api/docs/appendix/geotargeting
#https://developers.google.com/adwords/api/docs/reference/v201809/TargetingIdeaService.TargetingIdeaSelector

import _locale, sqlite3, googleads, traceback, time, os
import pandas as pd
from googleads import adwords
from googleads import oauth2
from ads_prepare import create_db_ads
from dotenv import load_dotenv
load_dotenv()

n_keywords = 100

create_db_ads()

db_name_keyword = os.environ.get("db_name_keyword_ads")

def select_keyword():
    print('-------------------------')
    conn = sqlite3.connect(db_name_keyword)
    c = conn.cursor()
    global keywords_list_db
    keywords_list_db = []
    for x in range(0, n_keywords):
        data = pd.read_sql_query("SELECT KEYWORDS FROM KEYWORDS_LIST WHERE SUM <> 2 AND CHECKING = 0 LIMIT 1;", conn)
        #print(type(data['KEYWORDS'].iat[0]))
        keyword = (data['KEYWORDS'].iat[0])
        keywords_list_db.append(keyword)
        c.execute("Update KEYWORDS_LIST set CHECKING = 1 where KEYWORDS = ?", (keyword,))
    conn.commit()
    conn.close()
    print(keywords_list_db)



#locations_id = '2156' #Cina CN
locations_id = '2380' #Italia IT
#locations_id = '2076' #Brasile BR
#locations_id = '2250' #Francia FR
#locations_id = '2840' #America US
#locations_id = '2620' #Portogallo PT
#locations_id = '2124' #Canada CA
#locations_id = '2710' #Sudsfrica ZA
#locations_id = '2826' #Gran Bretagna GB
#locations_id = '2250' #Francia FR
#locations_id = '2276' #Germania DE
#locations_id = '2643' #Russia RU
#locations_id = '2643' #Australia AU
#locations_id = '2392' #Giappone JP
#locations_id = '2792' #Turchia TR
#locations_id = '2724' #Spagna ES
#locations_id = '2484' #Messico MX

_locale._getdefaultlocale = (lambda *args: ['it_IT', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['zh_CN', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['fr_FR', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['pt-BR', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['pt_PT', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['en-CA', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['en-ZA', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['en-GB', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['en-US', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['de-DE', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['ru-RU', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['en-AU', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['ja-JP', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['tr-TR', 'UTF-8'])
#_locale._getdefaultlocale = (lambda *args: ['es-MX', 'UTF-8'])

#print(_locale._getdefaultlocale())

class searchVolumePuller ( ):
    def __init__(self, client_ID, client_secret, refresh_token, developer_token, client_customer_id):
        self.client_ID = client_ID
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.developer_token = developer_token
        self.client_customer_id = client_customer_id

    def get_client(self):
        access_token = oauth2.GoogleRefreshTokenClient (self.client_ID,
                                                        self.client_secret,
                                                        self.refresh_token)
        adwords_client = adwords.AdWordsClient (self.developer_token,
                                                access_token,
                                                client_customer_id=self.client_customer_id,
                                                cache=googleads.common.ZeepServiceProxy.NO_CACHE)

        return adwords_client

    def get_service(self, service, client):

        return client.GetService (service)

    def get_search_volume(self, service_client, keyword_list):
        # empty dataframe to append data into and keywords and search volume lists#
        keywords = []
        search_volume = []
        categories = []
        competitions = []
        average_cpc = []
        targeted_monthly_searches = []
        keywords_and_search_volume = pd.DataFrame ( )
        # need to split data into smaller lists of 700#
        sublists = [keyword_list[x:x + 700] for x in range (0, len (keyword_list), 700)]
        for sublist in sublists:

            # Construct selector and get keyword stats.
            selector = {
                'ideaType': 'KEYWORD',
                'requestType': 'STATS',
            }

            # select attributes we want to retrieve#
            selector['requestedAttributeTypes'] = [
                'KEYWORD_TEXT',
                'SEARCH_VOLUME',
                'COMPETITION',
                'CATEGORY_PRODUCTS_AND_SERVICES',
                'AVERAGE_CPC',
                'TARGETED_MONTHLY_SEARCHES',
                #'IDEA_TYPE'
                ]

            # configure selectors paging limit to limit number of results#
            offset = 0
            selector['paging'] = {
                'startIndex': str (offset),
                'numberResults': str (len (sublist))
            }

            # specify selectors keywords to suggest for#
            selector['searchParameters'] = [{
                'xsi_type': 'RelatedToQuerySearchParameter',
                'queries': sublist
            }]
            
            # Location setting (optional).
            selector['searchParameters'].append({
                'xsi_type': 'LocationSearchParameter',
                'locations': [{'id': f'{locations_id}'}]
            })

            # Network search parameter (optional)
            selector['searchParameters'].append({
                'xsi_type': 'NetworkSearchParameter',
                'networkSetting': {
                    'targetGoogleSearch': True,
                    'targetSearchNetwork': False,
                    'targetContentNetwork': False,
                    'targetPartnerSearchNetwork': False
                }
            })

            '''
            selector['searchParameters'].append({
                'matchType': 'EXACT'
            })
            '''

            # pull the data#
            page = service_client.get(selector)
            # print(page)
            # access json elements to return the suggestions#
            for i in range (0, len (page['entries'])):
                #keywords
                keywords_from_json= page['entries'][i]['data'][0]['value']['value']
                #print(keywords_from_json)
                keywords.append(keywords_from_json)
                #categorie
                categories_from_json= page['entries'][i]['data'][1]['value']['value']
                #print(categories_from_json)
                categories.append(categories_from_json)
                #competition
                competitions_from_json= page['entries'][i]['data'][2]['value']['value']
                #print(competitions_from_json)
                competitions.append(competitions_from_json)
                #Volume di riceca mensile
                targeted_monthly_searches_from_json= page['entries'][i]['data'][3]['value']['value']
                #print(targeted_monthly_searches_from_json)
                targeted_monthly_searches.append(targeted_monthly_searches_from_json)
                #cpc medio
                microAmount = 'microAmount'
                try:
                    if microAmount in page['entries'][i]['data'][4]['value']['value']: 
                        average_cpc_from_json= page['entries'][i]['data'][4]['value']['value']['microAmount']
                        # print(average_cpc_from_json)
                        average_cpc.append(average_cpc_from_json)
                except:
                    average_cpc_from_json= 0
                    average_cpc.append(average_cpc_from_json)
                #volume di ricerca
                search_volume_from_json= page['entries'][i]['data'][5]['value']['value']
                #print(search_volume_from_json)
                search_volume.append(search_volume_from_json)

        keywords_and_search_volume['Keywords'] = keywords
        keywords_and_search_volume['Search Volume'] = search_volume
        keywords_and_search_volume['Category'] = categories
        keywords_and_search_volume['Competition'] = competitions
        keywords_and_search_volume['Average CPC'] = average_cpc
        keywords_and_search_volume['Monthly Searches'] = targeted_monthly_searches

        #keywords_and_search_volume['Average CPC'] = average_cpc
        return keywords_and_search_volume

if __name__ == '__main__':
    CLIENT_ID = os.environ.get("CLIENT_ID_ADS")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET_ADS")
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN_ADS")
    DEVELOPER_TOKEN = os.environ.get("DEVELOPER_TOKEN_ADS")
    CLIENT_CUSTOMER_ID = os.environ.get("CLIENT_CUSTOMER_ID_ADS")

    timestr = time.strftime('%Y%m%d-%H%M%S')
    #print(timestr)


    while True:
        try:
            select_keyword()
            volume_puller = searchVolumePuller(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, DEVELOPER_TOKEN, CLIENT_CUSTOMER_ID)
            adwords_client = volume_puller.get_client ( )
            targeting_service = volume_puller.get_service ('TargetingIdeaService', adwords_client)
            kw_sv_df = volume_puller.get_search_volume (targeting_service, keywords_list_db)
            #kw_sv_df = pd.json_normalize(kw_sv_df2['Monthly Searches'])
            print(kw_sv_df)
            my_file = 'output_data/6_google_ads_export-Volume.csv'
            isfile = os.path.isfile(my_file)
            #print(isfile)
            if isfile == False:
                # path exists
                kw_sv_df.to_csv(my_file, index=False, encoding='utf-8', sep='\t', decimal=',')
            else:
                kw_sv_df.to_csv(my_file, mode='a', index=False, header=False, encoding='utf-8', sep='\t', decimal=',')
            print('pausa 10 secondi')
            time.sleep(10)
        except:
            for kw in keywords_list_db:
                conn = sqlite3.connect(db_name_keyword)
                c = conn.cursor()
                c.execute("Update KEYWORDS_LIST set CHECKING = 0 where KEYWORDS = ?",(kw,))
                conn.commit()

            print('pausa 35 secondi')
            time.sleep(35)
