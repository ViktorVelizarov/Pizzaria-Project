#here we store our DB models

from . import db
from flask_login import UserMixin   #this allows us to get data about the currently logged user in other files
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)     #primary key
    email = db.Column(db.String(150), unique=True)   #150 is maximum lenght, unique means no user can have the same email as another one
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150), default="client")   #client by default, can only be set to admin from the DB itself
    orders = db.relationship('Order')             #everytime we create an order, its id is added to this field of the given user
    
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #primary key
    name = db.Column(db.String(150))
    image = db.Column(db.String(150))
    ingredients = db.Column(db.String(500))

    cost = db.Column(db.Float)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #primary key
    date = db.Column(db.DateTime(timezone=True), default=func.now())  #current date
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))         #foreign key
    status = db.Column(db.String(150))
    orderedItems = db.Column(db.String(500))
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))         #foreign key
    content = db.Column(db.String(500))
    
    