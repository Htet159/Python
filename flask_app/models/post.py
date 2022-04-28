from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Post:
    db = "portfolio_model"

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

    @classmethod
    def edit_post(cls, data):
        query = "UPDATE posts SET content = %(content)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def like_or_unlike_post(cls, data):
        pre_query = "SELECT * FROM likes WHERE post_id = %(p_id)s and user_id = %(u_id)s;"
        results = connectToMySQL(cls.db).query_db(pre_query, data)
        if len(results) <= 0:
            query = "INSERT INTO likes(user_id, post_id) VALUES(%(u_id)s, %(p_id)s);"
            return connectToMySQL(cls.db).query_db(query, data)
        else:
            query_2 = "DELETE FROM likes WHERE post_id = %(p_id)s and user_id = %(u_id)s;"
            return connectToMySQL(cls.db).query_db(query_2, data)

    @classmethod
    def all_posts_with_likes_and_users(cls):
        query = "SELECT posts.*, users.first_name, users.last_name, count(likes.id) AS likes FROM posts LEFT JOIN likes ON posts.id = post_id LEFT JOIN users ON posts.user_id = users.id GROUP BY posts.id;" #this grabs the necessary post along with the associated likes and users.
        results = connectToMySQL(cls.db).query_db(query) # make the database results into a variable "results"
        posts = []
        for post_row in results:
            user_id = { #data dictionary for login data 
                'first_name' : post_row['first_name'],
                'last_name' : post_row['last_name']
            }
            post_data = {
                "id" : post_row['id'],
                "likes" : post_row['likes'],
                "content" : post_row['content'],
                "created_at" : post_row['created_at'],
                "updated_at" : post_row['updated_at'],
                'user_id' : user_id
            }
            posts.append(post_data)
        return posts

    @classmethod
    def get_post_with_user_by_id(cls, data):
        query = "SELECT posts.*, users.first_name, users.last_name FROM posts LEFT JOIN users ON user_id = users.id WHERE user_id =  %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        posts = []
        for post_row in results:
            post_data = {
                "id" : post_row['id'],
                "content" : post_row['content'],
                "created_at" : post_row['created_at'],
                "updated_at" : post_row['updated_at'],
                'first_name' : post_row['first_name'],
                'last_name' : post_row['last_name'],
                "user_id" : post_row['user_id']
            }
            posts.append(post_data)
        return posts

    @classmethod
    def get_post_by_id(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0]

    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)