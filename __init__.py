# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def queryStatsFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window

    results = []

    for flag_id in range(0, 4):
        id_list = mw.col.find_cards(f'flag:{flag_id}')
        if len(id_list) > 0:
            results.append(f'flag {flag_id}: {len(id_list)} cards')

    # insert API call to Todoist here

    # show a message box
    showInfo('\n'.join(results))

# create a new menu item, "test"
action = QAction("Query Stats", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, queryStatsFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)