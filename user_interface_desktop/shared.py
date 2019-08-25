from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QComboBox, QGroupBox, QGridLayout

from thsr.hsr.config import RESOURCES_DIR


def db_selector_0(items, country_label='Please select a database:',
                  init_index=0):
    label = QLabel(country_label)
    combo = QComboBox()
    for i in items:
        combo.addItem(i)
    combo.setCurrentIndex(init_index)
    return [[label], [combo]]


def grid_layout_0(widgets2d):
    gl = QGridLayout()
    n = len(widgets2d)
    for i in range(n):
        k = 0
        for j in widgets2d[i]:
            k += 1
            gl.addWidget(j, i, k)
    return gl


def grid_group_0(widgets2d, group_title=''):
    gl = grid_layout_0(widgets2d)
    gb = QGroupBox(group_title)
    gb.setLayout(gl)
    return gb


def teggs_logo_0():
    pixmap = QPixmap(RESOURCES_DIR+'graphics/logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    return logo
