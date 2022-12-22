import sys
import os 
import socket
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtNetwork import QTcpSocket

from server.database import database
from security import hash_password, compare_hashes

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('client/desktop/GUI/login.ui', self) 

        self.email.setMaxLength(45)
        self.email.returnPressed.connect(self.password.setFocus)

        self.password.setMaxLength(45)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.logIn)

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
        all_user_data = database.get_all_user()
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

        self.email.setMaxLength(45)
        self.password.setMaxLength(45)
        self.confirm_password.setMaxLength(45)
        self.first_name.setMaxLength(45)
        self.last_name.setMaxLength(45)

        self.email.returnPressed.connect(self.password.setFocus)
        self.password.returnPressed.connect(self.confirm_password.setFocus)
        self.confirm_password.returnPressed.connect(self.first_name.setFocus)
        self.first_name.returnPressed.connect(self.last_name.setFocus)

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
        user_data = database.get_all_user()
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
        self.send_button.clicked.connect(self.sendMessage)
        self.text_field.returnPressed.connect(self.sendMessage)
        self.text_field.setMaxLength(100)

        self.setUpAvatar()
        self.setUpFriendLayout()
        self.setUpServerConnection()

    def setUpFriendLayout(self):
        # set up toggle button
        self.show_friend = False
        self.text_browser.raise_()
        self.friend_button.clicked.connect(self.toggleFriendButton)

        # add all friends to list
        self.friend_list = [] 
        friend_id = []
        friendships = database.get_friendship(user_data['id'])

        for friendship in friendships:
            if user_data['id'] == friendship['user_id']:
                friend_id.append(friendship['friend_id'])
            else:
                friend_id.append(friendship['user_id'])

        for id in friend_id:
            self.friend_list.append(f"{database.get_user(id)[0]['first_name']} {database.get_user(id)[0]['last_name']}")

        # convert friend list to UI button
        for friend in self.friend_list:
            friend_widget = FriendWidget(friend)
            self.friend_layout.addWidget(friend_widget)

        # format layout 
        self.friend_layout.setSpacing(0)
        self.friend_layout.setContentsMargins(0, 0, 0, 0)

    def toggleFriendButton(self):
        if self.show_friend:
            self.text_browser.raise_()
            self. show_friend = False 
        else:
            self.text_browser.lower()
            self. show_friend = True

    def setUpAvatar(self):
        self.name.setText(f"{user_data['first_name']} {user_data['last_name']}")

        
        try: 
            path = database.get_avatar(user_data['id'])['path']
            
            if not os.path.isfile(path): 
                raise FileNotFoundError

        except Exception:
            # default image
            path = 'client/desktop/GUI/Resource/default_avatar.png'

        pixmap = QPixmap(path)
        avatar = QIcon(pixmap)
        
        self.avatar.setIcon(avatar)

    def setUpServerConnection(self):
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
        '''
        DATA FORMAT: Dictionary
        {
            "type": "private"/"public"
            "sender": user_id,
            "receiver": friend_id, 
            "message": message
        }
        '''
        # text = self.text_field.toMarkdown().strip() # formated text 
        debug_text = self.text_field.text().strip()

        if not len(debug_text):
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

class FriendWidget(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.button = QPushButton(name, self)
        self.button.setStyleSheet("border-radius: 20px; background-color: rgb(246, 224, 181); font: 75 18pt 'MS Shell Dlg 2';")
        self.layout.addWidget(self.button)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

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
