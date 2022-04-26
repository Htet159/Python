from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user



class Friend:
    def __inti__(self, data):
        self.db = "portfolio_model"
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users = []

    @classmethod
    def save_friend(cls, data):
        query = "INSERT INTO friends (user_id, friend_id) VALUES(%(u_id)s, %(fr_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_friends_with_users(cls, data):
        query = "SELECT * FROM users JOIN friends ON users.id = user_id JOIN user ON friend_id = users.id WHERE friend_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        friend = cls(results[0])
        for row in results:
            user_data = {
                "id" : row['user.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at']
            }
            friend.users.append(user.User(user_data))
        return friend

    @classmethod
    def get_strangers_by_user(cls, data):
        query = "SELECT * FROM users JOIN friends ON users.id = user_id JOIN user ON friend_id = users.id NOT IN (%(id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def remove_friend(cls, data):
        query = "DELETE FROM friends WHERE friend_id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)