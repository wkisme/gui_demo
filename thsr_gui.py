from PyQt5.QtWidgets import QApplication

from hsr.user_interface.user_window import user_window_0

if __name__ == '__main__':
    app = QApplication([])
    uw = user_window_0()
    uw.show()
    app.exec_()
