from flask_app import app
from flask import flash
from flask import request, render_template, redirect, session, flash
from flask_app.models.show import Show
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def dash():
    id = {'id': session['user_id']}
    return render_template("dashboard.html", shows = Show.get_all_shows_by_user(id), user = User.get_user_by_id(id))

@app.route('/show/delete/<int:id>')
def remove(id):
    data = {
        "id": id
    }
    Show.delete_show(data)
    return redirect('/dashboard')

@app.route('/show/new')
def new_show():
    if 'user_id' not in session:
        flash("You must be signed in to view this page.")
        return redirect('/logout')
    return render_template("new_show.html")

@app.route('/show/add', methods = ["POST"])
def add_show():
    if 'user_id' not in session:
        flash("You must be signed in to complete this action.")
        return redirect('/logout')
    if not Show.show_validation(request.form):
        return redirect('/show/new')
    data = {
        'title':request.form['title'],
        'network':request.form['network'],
        'description':request.form['description'],
        'release_date':request.form['release_date'],
        'user_id': session['user_id']
    }
    Show.save_show(data)
    return redirect('/dashboard')

@app.route('/view/show/<int:id>')
def this_show(id):
    data = {
        "id": id
    }
    id = {"id":session['user_id']}
    return render_template("this_show.html", show = Show.get_show_by_id(data), user = User.get_user_by_id(id))

@app.route('/show/edit/<int:id>')
def edit_show(id):
    data = {
        "id": id
    }
    return render_template("edit_show.html", show = Show.get_show_by_id(data))

@app.route('/show/change', methods = ["POST"])
def change():
    if 'user_id' not in session:
        flash("You must be signed in to complete this action.")
        return redirect('/logout')
    if not Show.show_validation(request.form):
        return redirect('/show/new')
    data = {
        'title':request.form['title'],
        'network':request.form['network'],
        'description':request.form['description'],
        'release_date':request.form['release_date'],
        'id': request.form['id']
    }
    Show.edit_show(data)
    return redirect('/dashboard')

