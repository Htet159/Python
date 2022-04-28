from distutils.command.build_scripts import first_line_re
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def log_and_reg():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/register', methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    register_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(register_data)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login', methods=["POST"])
def login_user():
    user_data = {
        'email': request.form['email']
    }
    user = User.get_user_by_email(user_data)
    if not user:
        flash('Invalid Email Address or Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']): #if the hashed password does not match the hashed password submitted
        flash('Invalid Email Address or Password', 'login')
        return redirect('/')
    session['user_id'] = user.id #place login id into sessions
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id']
    }
    user = User.get_user_by_id(data)  #grabs login information using login id from sessions
    posts = Post.all_posts_with_likes_and_users() #grabs all posts with their user information and their cheer information
    friends_suggest = User.allFriendSuggestions(data)# for now showing all friends not friends with (no mutuals)
    
    return render_template('dashboard.html' , user = user, posts = posts, friends_suggest = friends_suggest) #connects html and brings in variables into html

@app.route('/addfriend/<int:id>')
def addfriend(id):
    data ={
        'user_id': session['user_id'],
        'following_id': id
    }
    User.addFriend(data)
    return redirect('/dashboard')

@app.route('/removefriend/<int:id>')
def removefriend(id):
    data ={
        'user_id': session['user_id'],
        'following_id': id
    }
    User.removeFriend(data)
    return redirect('/profile')



@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id']
    }
    user = User.get_user_by_id(data)
    friends = User.usersFriends(data)
    return render_template('profile.html' , user = user, friends = friends) #connects html and brings in variables into html

@app.route('/user/posts')
def posts():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template('user_posts.html' , user = user) 


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/like/<int:id>")
def like_action(id):
    if 'user_id' not in session:
        flash("You must be signed in to view this page.")
        return redirect('/logout')
    data = {
        "p_id" : id,
        "u_id" : session['user_id']
    }
    Post.like_or_unlike_post(data)
    return redirect("/dashboard")
