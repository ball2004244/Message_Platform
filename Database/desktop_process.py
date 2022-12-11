import mysql.connector

class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'test_user'
        self.password = '12345678'
        self.port = '3306'
        self.database = 'test_db'
        self.con = None

    def connect(self):
        self.con = mysql.connector.connect(host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)
    
    def get_all_data(self):
        try:
            self.connect()
            cursor = self.con.cursor(dictionary=True)
            sql = 'SELECT * FROM test_table'
            cursor.execute(sql)
            result = cursor.fetchall() 

            return result 

        except Exception as e:
            print('Fail to get data from DATABASE')
            print(e)
        
        finally:
            if self.con:
                self.con.close()