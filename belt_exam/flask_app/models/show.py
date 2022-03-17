from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Show:
    db = "tv_show_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save_show(cls, data):
        query = "INSERT INTO tv_shows(title, network, release_date, description, user_id) VALUES(%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_shows_by_user(cls, data):
        query = "SELECT * FROM tv_shows JOIN users ON tv_shows.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        all_shows = []
        for row in results:
            one_show = cls(row)
            one_show_user_info = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            one_show.user = User(one_show_user_info)
            all_shows.append(row)
        return all_shows

    @classmethod
    def get_show_by_id(cls, data):
        query = "SElECT * FROM tv_shows WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results [0]

    @classmethod
    def edit_show(cls, data):
        query = "UPDATE tv_shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM tv_shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)



    @staticmethod
    def show_validation(show):
        is_valid = True
        if len(show['title']) < 1 :
            flash("Title is required.", "show")
            is_valid = False
        if 1 < len(show['title']) < 3 :
            flash("Title must have more than 3 characters.", "show")
            is_valid = False
        if len(show['network']) < 1 :
            flash("Network must have more than 3 characters.", "show")
            is_valid = False
        if 1 < len(show['network']) < 3 :
            flash("Network is a required.", "show")
            is_valid = False
        if len(show['release_date']) < 1 :
            flash("Date created is a required field.", "show")
            is_valid = False
        if len(show['description']) < 1 :
            flash("Description is a required field.")
            is_valid = False
        if 1 < len(show['description']) < 3 :
            flash("Description must have more than 3 characters.", "show")
            is_valid = False
        return is_valid
