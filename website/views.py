#here we put our views/ URL endpoints 

#a blueprint in py is just a file that stores the routes of our app
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Pizza
from . import db
from .models import Pizza, Order, Cart
import json
from datetime import datetime

views = Blueprint('views', __name__)     #we create a BP named views

selected_pizzas = [] 
selected_prices = [] 
currentOrder = []


@views.route('/', methods=['GET', 'POST'])  #defining a route 
@login_required
def home():
    pizzas = Pizza.query.all()
    return render_template("home.html",user=current_user, pizzas=pizzas) #send the curr user to home template


@views.route('/cart', methods=['GET', 'POST'])  #cart route
@login_required
def cart():
    #if its a POST req
    if request.method == 'POST': 
        pizza_name = request.form.get('pizzaName')
        pizza_cost = request.form.get('pizzaCost')
        selected_pizzas.append(pizza_name)      #add the selected pizza to the array
        selected_prices.append(pizza_cost)
        
        pizzas = Pizza.query.all()
                                                       #we use a delimiter because we cant use array fields in sqlite
        userCart = Cart.query.filter_by(user_id=current_user.id).first() #search if the current user already has a cart property
        if userCart:                                                     #if yes, just update its content                         
            userCart.content += ', ' + pizza_name
            userCart.content_prices += ', ' + pizza_cost
            db.session.commit()
            
        else:                                                            #if no, create one
            new_cart = Cart(user_id=current_user.id, content=pizza_name, content_prices=pizza_cost)     #create new user and hash his password, sha256 is a hashind method
            db.session.add(new_cart)                                     #add the new order to the DB
            db.session.commit() 
            
        return render_template("home.html",user=current_user, pizzas=pizzas) 
    
    #if its a GET req
    userCart = Cart.query.filter_by(user_id=current_user.id).first()
    if userCart:
        pizzasInCart = userCart.content
        costsInCart = userCart.content_prices
        totalCost = round(sum(float(price) for price in selected_prices), 2)
    else:
        pizzasInCart = ""
        costsInCart = ""
        totalCost = ""
    return render_template("cart.html", user=current_user, pizza = pizzasInCart, costs=costsInCart, totalCost=totalCost ) 


@views.route('/order-number', methods=['GET']) 
@login_required
def orderNumber():
    global currentOrder
    print("current order in waiting function")
    print(currentOrder)
    return render_template("orderNumber.html", user=current_user, yourOrder=currentOrder)

@views.route('/pizzas/details' ,  methods=['GET', 'POST'])
def greet():
    pizza = []
    if request.method == 'POST':
        pizza = request.form.get('pizza')
        print(pizza)
        return render_template('details.html', pizza=pizza)
    else:

        return render_template('details.html', pizza=pizza)

@views.route('/orders-board', methods=['GET'])
@login_required
def ordersBoard():
    userOrders= Order.query.filter(Order.user_id == current_user.id).all()
    return render_template("ordersBoard.html", user=current_user, orders=userOrders)  

@views.route('/receive-orders', methods=['GET', 'POST'])  
@login_required
def receiveOrders():
    global currentOrder
    if request.method == 'POST': 
        currentOrderInfo = request.form.get('currentOrder')
        new_order = Order(date=datetime.now(), user_id=current_user.id, status="Pending",  orderedItems = currentOrderInfo)     #create new user and hash his password, sha256 is a hashind method
        db.session.add(new_order)             #add the new order to the DB
        db.session.commit()   
        currentOrder = new_order  
        selected_pizzas.clear() #clear local list cart
        selected_prices.clear()
        
        #clear DB cart
        delimiter = ", "    
        userCart = Cart.query.filter_by(user_id=current_user.id).first() 
        if userCart:                                                                       
            userCart.content = delimiter.join(selected_pizzas)
            userCart.content_prices = delimiter.join(selected_prices)
            db.session.commit()
        
        allOrders = Order.query.all()
        
        return render_template("orderNumber.html", user=current_user, yourOrder=currentOrder, orders=allOrders) 
   
    else:
        allOrders = Order.query.all()  
        pending_orders = Order.query.filter(Order.status == "Pending").all()
        cooking_orders = Order.query.filter(Order.status == "In preparation").all()
        ready_orders = Order.query.filter(Order.status == "Ready").all()   
        return render_template("receiveOrders.html", user=current_user, pending_orders=pending_orders, cooking_orders=cooking_orders, ready_orders=ready_orders) 

@views.route('/remove_pizza', methods=['POST'])
@login_required
def remove_pizza():
    pizza_name = request.form.get('pizzaName')  
    if pizza_name in selected_pizzas:
        index = selected_pizzas.index(pizza_name)
        selected_pizzas.pop(index)
        selected_prices.pop(index)
        #selected_pizzas.remove(pizza_name)  
          
    
    #change the DB cart to match the new cart array
    delimiter = ", "    
    userCart = Cart.query.filter_by(user_id=current_user.id).first() 
    if userCart:                                                                       
        userCart.content = delimiter.join(selected_pizzas)
        userCart.content_prices = delimiter.join(selected_prices)
        db.session.commit()
        totalCost = round(sum(float(price) for price in selected_prices), 2)
    return render_template("cart.html", user=current_user, pizza = userCart.content, costs=userCart.content_prices, totalCost=totalCost)   

@views.route('/remove_all_pizzas', methods=['POST'])
@login_required
def remove_all_pizza():      
    #clear DB cart                                    
    userCart = Cart.query.filter_by(user_id=current_user.id).first() 
    selected_prices = ""
    totalCost = round(sum(float(price) for price in selected_prices), 2)
    if userCart:                                                                       
        userCart.content = ""
        userCart.content_prices = ""
        db.session.commit()
    return render_template("cart.html", user=current_user, pizza = userCart.content, prices=userCart.content_prices, totalCost=totalCost)  

@views.route('/start_order', methods=['POST'])
@login_required
def start_order():
    chosen_id = request.form.get('chosenOrder') 

    startedOrder = Order.query.get(chosen_id)       # Retrieve the order

    if startedOrder:                         # Check if the order exists
        startedOrder.status = "cooking"      # Update the status field    
        db.session.commit()                  # Commit the changes to the database

    allOrders = Order.query.all()
    pending_orders = Order.query.filter(Order.status == "Pending").all()
    cooking_orders = Order.query.filter(Order.status == "In preparation").all()
    ready_orders = Order.query.filter(Order.status == "Ready").all()
    return render_template("receiveOrders.html", user=current_user, pending_orders=pending_orders, cooking_orders=cooking_orders, ready_orders=ready_orders)

@views.route('/finish_order', methods=['POST'])
@login_required
def finish_order():
    chosen_id = request.form.get('chosenOrder') 

    startedOrder = Order.query.get(chosen_id)       # Retrieve the order

    if startedOrder:                         # Check if the order exists
        startedOrder.status = "Ready"      # Update the status field    
        db.session.commit()                  # Commit the changes to the database

    allOrders = Order.query.all()
    pending_orders = Order.query.filter(Order.status == "Pending").all()
    cooking_orders = Order.query.filter(Order.status == "In preparation").all()
    ready_orders = Order.query.filter(Order.status == "Ready").all()
    return render_template("receiveOrders.html", user=current_user, pending_orders=pending_orders, cooking_orders=cooking_orders, ready_orders=ready_orders)    
