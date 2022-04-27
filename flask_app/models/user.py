from turtle import fillcolor
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = "portfolio_model"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        # checks if email is already in the database
        query = "SELECT * FROM  users WHERE email = %(email)s ;"
        results = connectToMySQL('portfolio_model').query_db(query, user)
        if len(results) >= 1:  # if statement to check if email is already in the database
            flash("Email is already taken", 'register')
            is_valid = False
        if len(user['first_name']) < 1:
            flash("First name must be at least 2 characters", 'register')
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name must be at least 2 characters", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", 'register')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords must match", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", 'register')
            is_valid = False
        return is_valid

    @classmethod
    def usersFriends(cls,data):
        query = """SELECT friend.first_name, friend.last_name,following.* from users
        JOIN following  on users.id = user_id
        JOIN users as friend on following.following_id = friend.id
        where users.id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        friends =[]
        for result in results:
            friend_data = {
                'first_name':result['first_name'],
                'last_name':result['last_name'],
                'following_id': result['following_id']
            }
            friends.append(friend_data)
        print(friends)
        return friends

    @classmethod #just to get something on the html
    #there must be a way we can use if statements to track is this users id relateds to the following of the logins following_id's
    def allFriendSuggestions(cls,data):
        query ="""SELECT users.id, users.first_name, users.last_name, users.created_at from users
        join following on following.following_id = users.id
        join users as login on login.id = following.user_id 
        where following_id NOT IN(select following_id from following where user_id = %(id)s)
        and users.id != %(id)s ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        users = []
        for user in results:
            user = {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'created_at': user['created_at']
            }
            users.append(user)
        print(users)
        return users
    
    @classmethod
    def addFriend(cls,data):
        query = 'INSERT INTO following (user_id,following_id) VALUES (%(user_id)s,%(following_id)s);'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def removeFriend(cls,data):
        query = 'DELETE FROM following WHERE user_id = %(user_id)s AND following_id = %(following_id)s ;'
        return connectToMySQL(cls.db).query_db(query,data)





    # @staticmethod
    # def validate_login(user):
    #     is_valid = True
    #     data = {
    #         'email': user['email']
    #     }
    #     user_in_db = User.get_user_by_email(data)
    #     if not user_in_db:
    #         is_valid = False
    #     return is_valid

    @classmethod
    def like_or_unlike_post(cls, data):
        pre_query = "SELECT * FROM likes WHERE post_id = %(post_id)s;"
        results = connectToMySQL(cls.db).query_db(pre_query, data)
        if len(results) <= 0:
            query = "INSERT INTO likes(user_id, post_id) VALUES(%(user_id)s, %(post_id)s);"
            return connectToMySQL(cls.db).query_db(query, data)
        else:
            query_2 = "DELETE FROM likes WHERE post_id = %(post_id)s;"
            return connectToMySQL(cls.db).query_db(query_2, data)

