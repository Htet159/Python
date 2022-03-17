from flask_app import app
from flask import request, render_template, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect('/sign_in')

@app.route('/sign_in')
def sign_in():
    return render_template("login.html")

@app.route('/user/create', methods = ['POST'])
def add_user():
    v_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "pw_con": request.form['pw_con']
        }
    if not User.user_reg_validation(v_data):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/login', methods = ['POST'])
def login():
    user_in_db = User.get_user_by_email(request.form)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

