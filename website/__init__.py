#this file makes our website folder into a python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()        #initialize DB
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhddwedwa kjshkjdhdasdasdjs'               #this setting here encripts the cookies and session data of our app. The secret key is jsut a random string in our case
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'      #here we say that our DB is stored at the location of sqllite. This will store the DB in our website folder
    db.init_app(app)        #define our app for the DB

    from .views import views     #importing BPs
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')       #registering BPs
    app.register_blueprint(auth, url_prefix='/')        #the prefix means from which url start are the routes in the BP accessed, in our case we want them to be accessed from the default /

    from .models import User, Pizza
    
    with app.app_context():
        db.create_all()


    #here we manage our login python functions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'   #where should we redirect the user if he tries to access a restricted page
    login_manager.init_app(app)               #tell the login manager which app we are using

    @login_manager.user_loader                #here we tell the flask login how to load users
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):        #here we check if the DB already exists, so we dont accidently overide it and reset the data in it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
