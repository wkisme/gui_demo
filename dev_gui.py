from PyQt5.QtWidgets import QApplication

from hsr.user_interface.dev_window import developer_window_0

if __name__ == '__main__':
    app = QApplication([])
    w = developer_window_0()
    w.show()
    app.exec_()
