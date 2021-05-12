import aqt
# from aqt.utils import showInfo, qconnect
# from aqt.qt import *
import requests


def queryStatsFunction() -> None:

    # retrieve config
    # =====================
    config = aqt.mw.addonManager.getConfig(__name__)
    airtable_url_base = config['airtable_url_base']
    airtable_view = config['airtable_view']
    airtable_api_key = config['airtable_api_key']


    # list airtable records
    # =====================
    url_complete = f'{airtable_url_base}?view={airtable_view}'

    print(f'querying: {url_complete}')
    response = requests.get(url_complete, headers={'Authorization': f'Bearer {airtable_api_key}'})
    if response.status_code != 200:
        error_message = f'received error while querying {url_complete}: {response.content} status code: {response.status_code}'
        aqt.utils.showError(error_message)
    
    # we need to get the record id of airtable records, so we can update them
    record_id_map = {}
    data = response.json()
    for record in data['records']:
        record_id_map[record['fields']['Name']] = record['id']

    print(record_id_map)
    

    results = []

    for flag_id in range(0, 4):
        id_list = aqt.mw.col.find_cards(f'flag:{flag_id}')
        if len(id_list) > 0:
            results.append(f'flag {flag_id}: {len(id_list)} cards')

    # insert API call to Todoist here

    # show a message box
    aqt.utils.showInfo('\n'.join(results))

# create a new menu item, "test"
action = aqt.qt.QAction("Query Stats", aqt.mw)
# set it to call testFunction when it's clicked
aqt.utils.qconnect(action.triggered, queryStatsFunction)
# and add it to the tools menu
aqt.mw.form.menuTools.addAction(action)