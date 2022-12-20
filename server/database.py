import mysql.connector

class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '12345678'
        self.port = '3306'
        self.database = 'test_db'
        self.connector = None
        self.user_table = 'test_table'

    def connect(self) -> None:
        self.connector = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, port=self.port, database=self.database)

    def add_user(self, email: str, password: str, first_name: str, last_name: str) -> None:
        try:
            self.connect()
            cursor = self.connector.cursor()

            # get latest id
            query = f'SELECT MAX(id) FROM {self.user_table}'
            cursor.execute(query)
            id = cursor.fetchone()[0]
            
            if not id: 
                id = 1
            else:
                id += 1

            # add data to database
            query = f'INSERT INTO {self.database}.{self.user_table} (id, email, password, first_name, last_name) VALUES (%s, %s, %s, %s, %s)'
            values = (id, email, password, first_name, last_name)
            cursor.execute(query, values)

            self.connector.commit()
            cursor.close()

        except Exception as e:
            print('Fail to add data to DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def remove_data(self) -> None:
        pass

    def get_all_data(self) -> dict:
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.user_table}'
            cursor.execute(query)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print('Fail to get data from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

database = ConnectToMySQL()
if __name__ == '__main__':
    db = ConnectToMySQL()
    result = db.get_all_data()
    # db.add_user('test@gmail.com', ' 1234567', 'Test', 'One')
    
    if result:
        for row, item in enumerate(result):
            print(row + 1, item)
    else:
        print('No data got from database')
