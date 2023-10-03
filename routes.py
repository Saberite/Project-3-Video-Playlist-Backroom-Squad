'''
CS3250 - Software Development Methods and Tools - Fall 2023
Instructor: Thyago Mota
Student: Sayizana Worku
Description: Project 1
'''
from app import app, db, load_user
from app.models import User
from app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

# TODO #1: implement the sign-in functionality
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    form = SignUpForm()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        about = form.about.data
        passwd = form.passwd.data
        passwd_confirm = form.passwd_confirm.data
        user_exists = User.query.filter_by(id=id).first()
        if user_exists:
            user_existsmsg = 'A user with this ID exists already.'
        else:
            passwd = b"password"
            hashed_passwd = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
            new_user = User(id=id, name=name, about=about, passwd=hashed_passwd)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('users_signup.html', form=form, user_existsmsg=user_existsmsg)
    return render_template('users_signup.html', form=form)
    return '<p>TODO #1</p>'

# TODO #2: implement the sign-up functionality
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    return '<p>TODO #2</p>'
    
# TODO #3: implement the sign-out functionality
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))
    return '<p>TODO #3</p>'

@app.route('/users')
@login_required
def list_users(): 
    users = User.query.all()
    return render_template('users.html', users=users)