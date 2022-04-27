from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Post:
    db = "portfolio_sm"

    def __init__(self, data):  # __init__ for post class
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = None

    @classmethod
    def allPostsWithUserInfo(cls):
        query = "SELECT posts.*, users.first_name, users.last_name FROM posts JOIN users on posts.user_id = users.id;"
        # make the database results into a variable "results"
        results = connectToMySQL(cls.db).query_db(query)
        posts = []  # empty array
        for post in results:  # looping through results
            user_id = {  # data dictionary for login data
                'first_name': post['first_name'],
                'last_name': post['last_name']
            }
            post_data = {  # data dictionary for post data
                'id': post['id'],
                'content': post['content'],
                'created_at': post['created_at'],
                'updated_at': post['updated_at'],
                'user_id': user_id  # connecting login data into post data
            }
            posts.append((post_data))
        # print(posts)
        return posts

    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['content']) < 10:
            flash("Post must be at least 10 charecters", 'post')
            is_valid = False
        if len(data['user_id']) <= 0:
            flash('err', 'post')
            is_valid = False
        return is_valid

    @classmethod
    def post(cls, data):
        query = "INSERT INTO posts (content,user_id) VALUES(%(content)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
