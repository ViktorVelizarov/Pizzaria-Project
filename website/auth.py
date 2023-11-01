from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)  #we create a BP named auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':   #receive the login form data
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #find a user with that email
        if user:
            if check_password_hash(user.password, password): #check if the login password is coresponding to the hashed password in the DB 
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  #login user on the server using a ready function
                return redirect(url_for('views.home'))       #return to home page after login
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required  #you cant access this page if there is not logged user
def logout():
    logout_user()
    return redirect(url_for('auth.login'))      #go to login page after logout


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':        #get the sent form data
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() #making sure the email is not used
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))     #create new user and hash his password, sha256 is a hashind method
            db.session.add(new_user)             #add the new user to the DB
            db.session.commit()                  #commit changes to the DB 
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))       #redirect to home page

    return render_template("signup.html", user=current_user)
