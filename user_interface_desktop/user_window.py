import time
from functools import partial

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QGridLayout

from thsr.hsr.config import SOFTWARE_NAME
from thsr.hsr.config import SOFTWARE_VERSION
from thsr.hsr.hs_db.config import RESULT_RELEVANCE_COL_NAME
from thsr.hsr.hs_db.metadata import get_all_db_metadata, names_of_databases, get_single_db_metadata
from thsr.hsr.hs_retrievers.hs_code_retriever import hs_search
from thsr.hsr.user_interface_desktop.shared import db_selector_0, teggs_logo_0, grid_group_0

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


ALL_DB_METADATA = get_all_db_metadata()


def user_window_0():
    qd = QDialog()
    qd.setWindowTitle(SOFTWARE_NAME + ' ' + SOFTWARE_VERSION)
    qd.setGeometry(10, 10, WINDOW_WIDTH, WINDOW_HEIGHT)
    cn = names_of_databases(ALL_DB_METADATA)
    cs = db_selector_0(cn, init_index=37)
    qd.countries_combo = cs[1][0]
    csp = grid_group_0(cs, 'Country selector')
    dp = description_panel_0()
    qd.query_edit = dp[1][0]
    dpp = grid_group_0(dp, 'Commodity description')
    sp = search_panel_0()
    qd.search_button = sp[0][0]
    qd.clear_query_button = sp[0][1]
    qd.clear_results_button = sp[0][2]
    qd.time_label = sp[0][3]
    spp = grid_group_0(sp, 'Search tools')
    rp = result_panel_0()
    qd.results_label = rp[0][0]
    qd.table = rp[1][0]
    rpp = grid_group_0(rp, 'Results')
    widgets_0 = [[csp, teggs_logo_0()], [dpp], [spp]]
    group_0 = grid_group_0(widgets_0)
    layout = QGridLayout()
    layout.addWidget(group_0, 0, 0)
    layout.addWidget(rpp, 1, 0)
    qd.setLayout(layout)
    qd.query_edit.setFocus()
    qd.search_button.clicked.connect(partial(search_0, qd))
    qd.clear_query_button.clicked.connect(partial(clear_description, qd))
    qd.clear_results_button.clicked.connect(partial(clear_results, qd))
    return qd


def search_0(user_window):
    tic = time.time()
    text = user_window.query_edit.text()
    if text == '':
        user_window.results_label.setText('<font color=red>Please enter the description.</font>')
    else:
        ci = user_window.countries_combo.currentIndex()
        md = get_single_db_metadata(ALL_DB_METADATA, ci)
        results = hs_search(md, text)
        (nr, nc) = results.shape
        user_window.table.setRowCount(nr)
        user_window.table.setColumnCount(nc)
        cols = results.columns.values
        if nr > 1:
            user_window.results_label.setText('The results:')
        elif nr == 0:
            user_window.results_label.setText('<font color=red>No results.</font>')
        else:
            user_window.results_label.setText('The result:')
        for j in range(nc):
            head_item = QTableWidgetItem(cols[j])
            user_window.table.setHorizontalHeaderItem(j, head_item)
        for i in range(nr):
            for j in range(nc):
                if cols[j] == RESULT_RELEVANCE_COL_NAME:
                    r = str("%.2f" % results.iat[i, j])
                else:
                    r = str(results.iat[i, j])
                item = QTableWidgetItem(r)
                user_window.table.setItem(i, j, item)
        user_window.table.resizeColumnToContents(0)
        user_window.table.setColumnWidth(1, WINDOW_WIDTH - 250)
        for c in range(2, nc):
            user_window.table.resizeColumnToContents(c)
        user_window.table.setColumnWidth(1, WINDOW_WIDTH - 250)
        for i in range(nr):
            user_window.table.resizeRowToContents(i)
        toc = time.time() - tic
        user_window.time_label.setText('Search time: ' + str('%.1f' % toc) + ' sec.')


def clear_results(user_window):
    user_window.table.clear()
    user_window.results_label.setText('')
    user_window.time_label.setText('')


def clear_description(user_window):
    user_window.query_edit.setText('')
    user_window.query_edit.setFocus()


def description_panel_0():
    label = QLabel('Please provide a commodity description:')
    edit = QLineEdit()
    return [[label], [edit]]


def search_panel_0():
    space_size = 40
    space = ''
    for i in range(space_size):
        space += ' '
    time_label = QLabel(space)
    search_button = QPushButton('Search')
    clear_results_button = QPushButton('Clear results')
    clear_desc_button = QPushButton('Clear description')
    search_tools = [[search_button, clear_desc_button, clear_results_button, time_label]]
    return search_tools


def result_panel_0():
    results_label = QLabel('')
    table = QTableWidget()
    return [[results_label], [table]]
