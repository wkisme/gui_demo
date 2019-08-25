from functools import partial

from PyQt5.QtWidgets import QDialog, QPushButton, QLabel

from hsr.config import SOFTWARE_NAME, SOFTWARE_VERSION
from hsr.evaluation.evaluator_0 import evaluate_0, alpha_score, epsilon_score
from hsr.hs_db.metadata import get_all_db_metadata, get_number_of_all_dbs, names_of_databases
from hsr.hs_db.preprocessor import preprocess_db
from hsr.user_interface_desktop.data_formatting import float_to_percent_str
from hsr.user_interface_desktop.shared import db_selector_0, grid_group_0, grid_layout_0, teggs_logo_0


ALL_DB_METADATA = get_all_db_metadata()


def developer_window_0():
    qd = QDialog()
    qd.setWindowTitle(SOFTWARE_NAME + ' ' + SOFTWARE_VERSION + ' Developer tools')
    cn = names_of_databases(ALL_DB_METADATA)
    cs = country_selector_1(cn, 37)
    qd.countries_combo = cs[1][0]
    qd.db_index_label = cs[2][0]
    csp = grid_group_0(cs, 'Country selector')
    dt = dev_tools_0()
    qd.import_single_db_button = dt[0][0]
    qd.import_all_db_button = dt[0][1]
    dtp = grid_group_0(dt, 'Database preprocessing tools')
    et = eval_tools()
    qd.eval_button_alpha = et[0][0]
    qd.eval_label_alpha = et[0][1]
    qd.eval_button_epsilon = et[1][0]
    qd.eval_label_epsilon = et[1][1]
    etp = grid_group_0(et, 'Evaluation tools')
    widgets = [[teggs_logo_0()],
               [csp],
               [dtp],
               [etp]]
    layout = grid_layout_0(widgets)
    qd.setLayout(layout)
    qd.import_single_db_button.clicked.connect(partial(import_single_db, qd))
    qd.import_all_db_button.clicked.connect(import_all_db)
    qd.eval_button_alpha.clicked.connect(partial(evaluate_alpha, qd))
    qd.eval_button_epsilon.clicked.connect(partial(evaluate_epsilon, qd))
    qd.countries_combo.currentIndexChanged.connect(partial(set_db_index_label, qd))
    return qd


def country_selector_1(items, init_index, country_label='Please select a database:'):
    cs = db_selector_0(items, country_label, init_index)
    index_label = QLabel('Database index: ' + str(init_index))
    cs.append([index_label])
    return cs


def dev_tools_0():
    import_single_db_button = QPushButton('Import single database')
    import_all_db_button = QPushButton('Import all databases')
    return [[import_single_db_button, import_all_db_button]]


def eval_tools():
    eval_button_alpha = QPushButton('Evaluate \u03B1-score')
    eval_label_alpha = QLabel('')
    eval_button_epsilon = QPushButton('Evaluate \u03B5-score')
    eval_label_epsilon = QLabel('')
    return [[eval_button_alpha, eval_label_alpha],
            [eval_button_epsilon, eval_label_epsilon]]


def import_single_db(user_window):
    db_index = user_window.countries_combo.currentIndex()
    preprocess_db(ALL_DB_METADATA, [db_index])


def import_all_db():
    n = get_number_of_all_dbs(ALL_DB_METADATA)
    preprocess_db(ALL_DB_METADATA, range(n))


def evaluate_alpha(user_window):
    db_index = user_window.countries_combo.currentIndex()
    user_window.eval_label_alpha.setText('\u03B1-score: ' +
                                         float_to_percent_str(evaluate_0(ALL_DB_METADATA, db_index, alpha_score)) + "%")


def evaluate_epsilon(user_window):
    db_index = user_window.countries_combo.currentIndex()
    user_window.eval_label_epsilon.setText('\u03B5-score: ' +
                                           float_to_percent_str(evaluate_0(ALL_DB_METADATA, db_index, epsilon_score))
                                           + "%")


def set_db_index_label(user_window):
    db_index = user_window.countries_combo.currentIndex()
    user_window.db_index_label.setText('Country index: ' + str(db_index))
