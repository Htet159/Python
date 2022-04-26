from crypt import methods
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import friend


@app.route('/delete/friend/<int:id>')
def friend_delete(id):
    data = {
        "id" : id
    }
    friend.Friend.remove_friend(data)
    return redirect("profile.html")

@app.route('/add/friend/<int:id>', methods = ["POST"])
def add_friend(id):
    data = {
        "fr_id" : id,
        "u_id" : session['user_id']
    }
    friend.Friend.save_friend(data)
    return redirect("dashboard.html")
