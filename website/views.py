#here we put our views/ URL endpoints 

#a blueprint in py is just a file that stores the routes of our app
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Pizza
import json

views = Blueprint('views', __name__)     #we create a BP named views

selected_pizzas = [] 
order = []


@views.route('/', methods=['GET', 'POST'])  #defining a route 
@login_required
def home():
    pizzas = Pizza.query.all()
    return render_template("home.html",user=current_user, pizzas=pizzas) #send the curr user to home template


@views.route('/cart', methods=['GET', 'POST'])  #cart route
@login_required
def cart():
    if request.method == 'POST': 
        pizza_name = request.form.get('pizzaName')
        selected_pizzas.append(pizza_name)
        pizzas = Pizza.query.all()
        return render_template("home.html",user=current_user, pizzas=pizzas) 
    return render_template("cart.html", user=current_user, pizza = selected_pizzas) 


@views.route('/waiting-page', methods=['GET'])  #waitingPage route
@login_required
def waitingPage():
    return render_template("waitingPage.html", user=current_user) 

@views.route('/receive-orders', methods=['GET', 'POST'])  #waitingPage route
@login_required
def receiveOrders():
    if request.method == 'POST': 
        currentOrder = request.form.get('currentOrder')
        order.append(currentOrder)
        selected_pizzas = []
        return render_template("cart.html", user=current_user, pizza = selected_pizzas) 
    return render_template("receiveOrders.html", user=current_user, order=order) 

@views.route('/remove_pizza', methods=['POST'])
@login_required
def remove_pizza():
    pizza_name = request.form.get('pizzaName')  
    if pizza_name in selected_pizzas:
         selected_pizzas.remove(pizza_name)   
    return render_template("cart.html", user=current_user, pizza = selected_pizzas)    