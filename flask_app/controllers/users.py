from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def log_and_reg():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    register_data = {
        'first_name': request.form['first_name'],
        'last_name' :request.form['last_name'],
        'email' : request.form['email'],
        'password': pw_hash
    }
    user_id = User.register_user(register_data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login' , methods=["POST"])
def login_user():
    if not User.validate_login(request.form):
        flash("Email and/or password is incorrect")
        return redirect('/')
    user_data = {
        'email' : request.form['email']
    }
    user = User.get_user_by_email(user_data)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash("Email and/or password is incorrect")
            return redirect('/')
        session['user_id'] = user.id
        return redirect('/dashboard')
    return redirect('/')

# @app.route('/dashboard')
# def dashboard():
#     user_data = {
#         'id' : session["user_id"]
#     }
#     return render_template("dashboard.html", user=User.get_user_by_id(user_data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

