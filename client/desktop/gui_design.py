import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEventLoop, QTimer
from PyQt5.QtNetwork import QTcpSocket

from server.database import database
from security import hash_password, compare_hashes

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('client/desktop/GUI/login.ui', self) 

        self.password.setEchoMode(QLineEdit.Password)

        self.login_button.clicked.connect(self.logIn)
        self.signup_button.clicked.connect(self.signUp)
        
        self.facebook_button.clicked.connect(self.authFacebook)
        self.instagram_button.clicked.connect(self.authInstagram)
        self.google_button.clicked.connect(self.authGoogle)
        self.snapchat_button.clicked.connect(self.authSnapchat)

    def logIn(self):
        # get email from input
        email = self.email.text().strip()
        password = self.password.text().strip()
        login = False

        if not (len(email) and len(password)):
            print('You must fill in both fields')
            login = False 

        # check if account already in database
        all_user_data = database.get_all_data()
        if all_user_data:
            for user in all_user_data:
                if email == user['email']:
                    # check if password matched
                    if compare_hashes(hash_password(password.encode('utf-8')), user['password']):
                        login = True
                        global user_data
                        user_data = {'id': user['id'], 'email': user['email'], 'first_name': user['first_name'], 'last_name': user['last_name']}
                        break
    
        if login:
            self.goToHomeScreen()
        else:
            print('Incorrect Email or Password')

    def authFacebook(self):
        print('Access Facebook')
    
    def authInstagram(self):
        print('Access Instagram')
    
    def authGoogle(self):
        print('Access Google')
    
    def authSnapchat(self):
        print('Access Snapchat')
    
    def goToHomeScreen(self):
        home_screen = HomeScreen()
        widget_stack.addWidget(home_screen)
        widget_stack.setCurrentIndex(1)

    def signUp(self):
        sign_up_screen = RegisterScreen()
        widget_stack.addWidget(sign_up_screen)
        widget_stack.setCurrentIndex(1)


class RegisterScreen(QMainWindow):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi('client/desktop/GUI/register.ui', self)
        self.login_button.clicked.connect(self.gotoLogIn)
        self.signup_button.clicked.connect(self.gotoSignUp)
        self.password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setEchoMode(QLineEdit.Password)

    def gotoSignUp(self):
        # get data from user input 
        email = self.email.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        register = True

        # check if all fields all filled
        if not (len(email) and len(password) and len(confirm_password) and len(first_name) and len(last_name)):
            print('You must fill all fields')
            register = False

        # check if password = confirm_password
        if password != confirm_password:
            print('Password did not match')
            register = False

        # check if account already in database
        user_data = database.get_all_data()
        for user in user_data:
            if email == user['email']:
                print('User existed, Try again')
                register = False

        # add account to database
        if register:
            #encrypt password
            encrypted_password = hash_password(password.encode('utf-8'))
            
            database.add_user(email, encrypted_password, first_name, last_name)
            self.gotoLogIn()

    def gotoLogIn(self):
        widget_stack.setCurrentIndex(0)
        widget_stack.removeWidget(widget_stack.widget(1))


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('client/desktop/GUI/home.ui', self)
        self.logout_button.clicked.connect(self.gotoLogIn)

        self.name.setText(f"Welcome {user_data['first_name']} {user_data['last_name']}")
        self.send_button.clicked.connect(self.sendMessage)

        # set up socket for message send-receive
        self.socket = QTcpSocket(self)

        # Get the local machine name
        # host = socket.gethostname()
        HOST, PORT = '127.0.0.1', 8000

        self.socket.connectToHost(HOST, PORT)

        # set up time that receive message every 3 seconds
        self.timer = QTimer()
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.receiveMessage)

        self.timer.start()

    def sendMessage(self):
        text = self.text_field.toMarkdown().strip() # formated text 
        debug_text = self.text_field.toPlainText().strip()

        if not len(text):
            print('Cannot sending blank text')
        else:
            print('client:', debug_text)

            #send message to server 
            message = f"{user_data['first_name']} {list(user_data['last_name'])[0]}: {debug_text}"
            self.socket.write(message.encode('utf-8')) 
            self.text_field.clear()
    
    def receiveMessage(self):
        # get message from server 
        if self.socket.bytesAvailable(): # only retrieve if there is > 0 bytes data
            message = self.socket.readAll().data()
            self.text_browser.append(message.decode('utf-8'))
        else:
            print('Looking For Data From Server')

    def gotoLogIn(self):
        #log out 
        self.socket.close()
        self.timer.stop()
        
        widget_stack.setCurrentIndex(0)
        widget_stack.removeWidget(widget_stack.widget(1))

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
