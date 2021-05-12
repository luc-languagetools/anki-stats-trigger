import aqt # for anki modules
import requests # for making requests to airtable


def queryStatsFunction() -> None:

    # retrieve config
    # =====================
    config = aqt.mw.addonManager.getConfig(__name__)
    airtable_url_base = config['airtable_url_base'] # looks like this: https://api.airtable.com/v0/appW777gjbRzAB60s/Stats
    # airtable_view = config['airtable_view'] # looks like this: Grid%20view
    airtable_api_key = config['airtable_api_key'] # should be in airtable account info


    # list airtable records
    # =====================
    # url_complete = f'{airtable_url_base}?view={airtable_view}'
    url_complete = airtable_url_base
    headers = {'Authorization': f'Bearer {airtable_api_key}'}

    print(f'querying: {url_complete}')
    response = requests.get(url_complete, headers=headers)
    if response.status_code != 200:
        error_message = f'received error while querying {url_complete}: {response.content} status code: {response.status_code}'
        aqt.utils.showCritical(error_message)
        return
    
    # we need to get the record id of airtable records, so we can update them
    record_id_map = {}
    data = response.json()
    for record in data['records']:
        record_id_map[record['fields']['Name']] = record['id']

    print(record_id_map)

    # collect data
    # ============

    update_records = []
    for flag_id in range(0, 4):
        id_list = aqt.mw.col.find_cards(f'flag:{flag_id}')
        field_name = f'flag {flag_id}'
        record_id = record_id_map[field_name]
        update_records.append({
            'id': record_id,
            'fields': {
                'Count': len(id_list)
            }
        })

    # update airtable
    # ===============

    update_data = {'records': update_records}
    print(update_data)
    response = requests.patch(airtable_url_base, json=update_data, headers=headers )
    if response.status_code != 200:
        error_message = f'received error while updating records: {airtable_url_base}: {response.content} status code: {response.status_code}'
        aqt.utils.showCritical(error_message)
        return



action = aqt.qt.QAction("Update Stats on Airtable", aqt.mw)
# call the queryStatsFunction when triggered
aqt.utils.qconnect(action.triggered, queryStatsFunction)
# and add it to the tools menu
aqt.mw.form.menuTools.addAction(action)