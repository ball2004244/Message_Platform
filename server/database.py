import mysql.connector

class ConnectToMySQL():
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'root'
        self.password = '12345678'
        self.port = '3306'
        self.database = 'test_db'
        self.user_table = 'user'
        self.friendship_table = 'friendship'
        self.avatar_table = 'avatar'
        self.connector = None

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
            print('Fail to add user to DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_user(self, id: int) -> dict:
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.user_table} WHERE id = {id}'
            cursor.execute(query)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print('Fail to get user from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_all_user(self) -> dict:
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)
            query = f'SELECT * FROM {self.database}.{self.user_table}'
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print('Fail to get all users from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def add_friendship(self, user_id: int, friend_id: int) -> None:
        try:
            self.connect()
            cursor = self.connector.cursor()

            # add data to database
            query = f"INSERT INTO {self.database}.{self.friendship_table} (user_id, friend_id) VALUES ({user_id}, {friend_id})"
 
            cursor.execute(query)

            self.connector.commit()

            cursor.close()

        except Exception as e:
            print('Fail to add new friendship to DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()
        pass 

    def get_friendship(self, id: int) -> dict:
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)

            query = f"SELECT * FROM {self.database}.{self.friendship_table} WHERE (user_id = {id} OR friend_id = {id});"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            # check if both friends are real users
            new_result = []
            for friendship in result:
                if (self.get_user(friendship['user_id']) and self.get_user(friendship['friend_id'])):
                    new_result.append(friendship)

            return new_result 
           

        except Exception as e:
            print('Fail to get friendship from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def delete_friendship(self, id: int) -> None:
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)

            query = f"DELETE FROM {self.database}.{self.friendship_table} WHERE (user_id = {id});"
            cursor.execute(query)

            self.connector.commit()
            cursor.close()

        except Exception as e:
            print('Fail to delete friendship from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

    def get_avatar(self, id: int) -> str:
        # get path to avatar stored in server storage
        try:
            self.connect()
            cursor = self.connector.cursor(dictionary=True)

            query = f"SELECT * FROM {self.database}.{self.avatar_table} WHERE user_id = {id}"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            if result:
               return result


        except Exception as e:
            print('Fail to get avatar path from DATABASE')
            print(e)

        finally:
            if self.connector:
                self.connector.close()

database = ConnectToMySQL()
if __name__ == '__main__':
    db = ConnectToMySQL()
    result = db.get_all_user()
    # db.add_user('test@gmail.com', ' 1234567', 'Test', 'One')

    # if result:
    #     for row, item in enumerate(result):
    #         print(row + 1, item)
    # else:
    #     print('No data got from database')

    friend_list = db.get_friendship(3)

    if friend_list:
        for row, item in enumerate(friend_list):
            print(row + 1, item)
    else:
        print('No data got from database')
    # print(db.get_avatar(1))