from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Like:
    def __init__(self, data):
        self.db = "portfolio_model"
        self.id = data['id']