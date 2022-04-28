from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/create/post', methods = ['POST'])
def createPost():
    data = {
        'content' : request.form['content'],
        'user_id': request.form['user_id']
    }
    if not Post.validate_post(data):
        return redirect('/dashboard')
    Post.post(data)
    return redirect('/dashboard')

@app.route("/edit/post/<int:id>", methods = ["POST"])
def this_post(id):
    data = {
        "id" : id
    }
    return render_template("edit_post.html", post = Post.get_post_with_user_by_id(data))