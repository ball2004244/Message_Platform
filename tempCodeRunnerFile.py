import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget

class TestScreen(QDialog):
    def __init__(self):
        super(TestScreen, self).__init__()
        loadUi('desktop.ui', self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_screen = TestScreen()

    widget = QStackedWidget()
    widget.addWidget(test_screen)

    widget.setFixedHeight(768)
    widget.setFixedWidth(1366)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')
