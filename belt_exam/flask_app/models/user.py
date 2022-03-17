from operator import is_
from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "tv_show_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.shows = []

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0]

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = '%(first_name)s', last_name = '%(last_name)s', email = '%(email)s', password = '%(password)s' WHERE id = %(id)s; "
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def user_reg_validation(user):
        is_valid = True
        users_info = User.get_all_users()
        if len(user['first_name']) < 1:
            flash("First Name is a required field.")
            is_valid = False
        if 1 < len(user['first_name']) < 3:
            flash("First Name must have 3 or more characters.")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last Name is a required field.")
            is_valid = False
        if 1 < len(user['last_name']) < 3:
            flash("Last Name must have 3 or more characters.")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email is a required field.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email address is invalid.")
            is_valid = False
        for row in users_info:
            if user['email'] == row['email']:
                flash("Email address is already in use.")
                is_valid = False
        if len(user['password']) < 1:
            flash("Password is a required field.")
            is_valid = False
        if user['pw_con'] != user['password']:
            flash("Password does not match.")
            is_valid = False
        if 1 < len(user['password']) < 8:
            flash("Password must contain more than 8 character.")
            is_valid = False
        return is_valid
    
    @staticmethod
    def user_login_validation(user):
        is_valid = True
        if len(user['email']) < 1:
            flash("Email is a required field.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email address is invalid.")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password is a required field.")
            is_valid = False
        return is_valid

