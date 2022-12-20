import sys
from database.database import *
from desktop.gui_design import *
from PyQt5.QtWidgets import QApplication, QStackedWidget

app = QApplication(sys.argv)
widget_stack = QStackedWidget()

login_screen = LoginScreen()

widget_stack.addWidget(login_screen)

widget_stack.setFixedHeight(800)
widget_stack.setFixedWidth(1000)
widget_stack.show()

try:
    sys.exit(app.exec_())
except:
    print('Exiting')