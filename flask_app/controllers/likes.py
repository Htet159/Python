from crypt import methods
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import user

@app.route("/like/<int:id>")
def like_action(id):
    if 'user_id' not in session:
        flash("You must be signed in to view this page.")
        return redirect('/logout')
    data = {
        "p_id" : id,
        "u_id" : session['user_id']
    }
    user.User.like_or_unlike_post(data)
    return redirect("/dashboard")
