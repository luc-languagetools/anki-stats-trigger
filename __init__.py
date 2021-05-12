import aqt # for anki modules
import requests # for making requests to airtable


def queryStatsFunction() -> None:

    # retrieve config
    # =====================
    config = aqt.mw.addonManager.getConfig(__name__)
    airtable_url = config['airtable_url_base'] # looks like this: https://api.airtable.com/v0/appW777gjbRzAB60s/Stats
    airtable_api_key = config['airtable_api_key'] # should be in airtable account info

    if len(airtable_url) == 0 or len(airtable_api_key) == 0:
        aqt.utils.showCritical('You must specify Airtable URL and API Key in the config')
        return

    # list airtable records
    # =====================
    headers = {'Authorization': f'Bearer {airtable_api_key}'}

    response = requests.get(airtable_url, headers=headers)
    if response.status_code != 200:
        error_message = f'received error while querying {airtable_url}: {response.content} status code: {response.status_code}'
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

    # count card in each flag
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
    # count suspended
    id_list = aqt.mw.col.find_cards('is:suspended')
    record_id = record_id_map['suspended']
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
    print(f'calling url: {airtable_url}')
    response = requests.patch(airtable_url, json=update_data, headers=headers )
    if response.status_code != 200:
        error_message = f'received error while updating records: {airtable_url}: {response.content} status code: {response.status_code}'
        aqt.utils.showCritical(error_message)
        return



action = aqt.qt.QAction("Update Stats on Airtable", aqt.mw)
# call the queryStatsFunction when triggered
aqt.utils.qconnect(action.triggered, queryStatsFunction)
# and add it to the tools menu
aqt.mw.form.menuTools.addAction(action)

# run this function on anki main window open
aqt.gui_hooks.main_window_did_init.append(queryStatsFunction)
# run this function after sync finish
aqt.gui_hooks.sync_did_finish.append(queryStatsFunction)
