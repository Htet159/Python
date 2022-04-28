from pkg_resources import EGG_DIST
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

@app.route("/edit/post/<int:id>")
def this_post(id):
    data = {
        "id" : id
    }
    return render_template("edit_post.html", posts = Post.get_post_by_id(data))

@app.route("/update/post", methods = ["POST"])
def update_post():
    data = {
        "id" : request.form['id'],
        "content" : request.form['content']
    }
    print(data)
    Post.edit_post(data)
    return redirect("/profile")

@app.route("/delete/post/<int:id>")
def bye_post(id):
    data = {
        "id" : id,
    }
    Post.delete_post(data)
    return redirect("/profile")