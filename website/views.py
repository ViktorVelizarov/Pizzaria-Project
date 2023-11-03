#here we put our views/ URL endpoints 

#a blueprint in py is just a file that stores the routes of our app
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from .models import Pizza
import json

views = Blueprint('views', __name__)     #we create a BP named views


@views.route('/', methods=['GET', 'POST'])  #defining a route 
@login_required
def home():
    pizzas = Pizza.query.all()
    print(pizzas)
    
    return render_template("home.html",user=current_user, pizzas=pizzas) #send the curr user to home template


@views.route('/cart', methods=['GET'])  #cart route
@login_required
def cart():
    return render_template("cart.html", user=current_user) 


@views.route('/waiting-page', methods=['GET'])  #waitingPage route
@login_required
def waitingPage():
    return render_template("waitingPage.html", user=current_user) 


@views.route('/receive-orders', methods=['GET'])  #waitingPage route
@login_required
def receiveOrders():
    return render_template("receiveOrders.html", user=current_user) 


@views.route('/pizzas/details' ,  methods=['GET', 'POST'])
def greet():
    pizza = []
    if request.method == 'POST':
        pizza = request.form.get('pizza')
        print(pizza)
        return render_template('details.html', pizza=pizza)
    else:

        return render_template('details.html', pizza=pizza)
