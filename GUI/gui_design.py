import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QMainWindow
from Database.desktop_process import ConnectToMySQL

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('GUI/login.ui', self)
        self.login_button.clicked.connect(self.logIn)
        self.signup_button.clicked.connect(self.signUp)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

    def logIn(self):
        # get email from input
        email = self.email.text()
        password = self.password.text()

        # check if gmail + password is True
        home_screen = HomeScreen()
        widget_stack.addWidget(home_screen)
        widget_stack.setCurrentIndex(1)
        #else do nothing
        
    def signUp(self):
        sign_up_screen = RegisterScreen()
        widget_stack.addWidget(sign_up_screen)
        widget_stack.setCurrentIndex(1)


class RegisterScreen(QMainWindow):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi('GUI/register.ui', self)
        self.login_button.clicked.connect(self.gotoLogIn)
        self.signup_button.clicked.connect(self.gotoSignUp)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)

    def gotoSignUp(self):
        # get data from user input 
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text() 
        first_name = self.first_name.text()
        last_name = self.last_name.text()


        # check if an account already in database
        # yes -> do nothing
        # no -> add account to database -> go to login
        self.gotoLogIn()

    def gotoLogIn(self):
        widget_stack.setCurrentIndex(0)
        widget_stack.removeWidget(widget_stack.widget(1))


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('GUI/home.ui', self)


if __name__ == '__main__':
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
