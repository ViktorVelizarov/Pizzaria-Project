#here we put our views/ URL endpoints 

#a blueprint in py is just a file that stores the routes of our app
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from . import db
from .models import Pizza, Order, Cart
import json
from datetime import datetime

views = Blueprint('views', __name__)     #we create a BP named views

selected_pizzas = [] 
order = []
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
        selected_pizzas.append(pizza_name)      #add the selected pizza to the array
        
        pizzas = Pizza.query.all()
                                                       #we use a delimiter because we cant use array fields in sqlite
        userCart = Cart.query.filter_by(user_id=current_user.id).first() #search if the current user already has a cart property
        if userCart:                                                     #if yes, just update its content                         
            userCart.content += ', ' + pizza_name
            db.session.commit()
            
        else:                                                            #if no, create one
            new_cart = Cart(user_id=current_user.id, content=pizza_name)     #create new user and hash his password, sha256 is a hashind method
            db.session.add(new_cart)                                     #add the new order to the DB
            db.session.commit() 
            
        return render_template("home.html",user=current_user, pizzas=pizzas) 
    
    #if its a GET req
    userCart = Cart.query.filter_by(user_id=current_user.id).first()
    if userCart:
        pizzasInCart = userCart.content
    else:
        pizzasInCart = ""
    return render_template("cart.html", user=current_user, pizza = pizzasInCart) 


@views.route('/order-number', methods=['GET']) 
@login_required
def orderNumber():
    global currentOrder
    print("current order in waiting function")
    print(currentOrder)
    return render_template("orderNumber.html", user=current_user, yourOrder=currentOrder)

@views.route('/orders-board', methods=['GET'])
@login_required
def ordersBoard():
    allOrders = Order.query.all()
    return render_template("ordersBoard.html", user=current_user, orders=allOrders)  

@views.route('/receive-orders', methods=['GET', 'POST'])  
@login_required
def receiveOrders():
    global currentOrder
    if request.method == 'POST': 
        
        new_order = Order(date=datetime.now(), user_id=current_user.id, status="pending")     #create new user and hash his password, sha256 is a hashind method
        db.session.add(new_order)             #add the new order to the DB
        db.session.commit()   
        currentOrder = new_order  
        
        currentOrderInfo = request.form.get('currentOrder')
        order.append({'id': new_order.id, 'orderInfo': currentOrderInfo})
        print(order)
        selected_pizzas.clear() #clear local list cart
        
        #clear DB cart
        delimiter = ", "    
        userCart = Cart.query.filter_by(user_id=current_user.id).first() 
        if userCart:                                                                       
            userCart.content = delimiter.join(selected_pizzas)
            db.session.commit()
        
        allOrders = Order.query.all()
        
        return render_template("orderNumber.html", user=current_user, yourOrder=currentOrder, orders=allOrders) 
    return render_template("receiveOrders.html", user=current_user, order=order) 

@views.route('/remove_pizza', methods=['POST'])
@login_required
def remove_pizza():
    pizza_name = request.form.get('pizzaName')  
    if pizza_name in selected_pizzas:
         selected_pizzas.remove(pizza_name)  
          
    
    #change the DB cart to match the new cart array
    delimiter = ", "    
    userCart = Cart.query.filter_by(user_id=current_user.id).first() 
    if userCart:                                                                       
        userCart.content = delimiter.join(selected_pizzas)
        db.session.commit()
    return render_template("cart.html", user=current_user, pizza = userCart.content)   

@views.route('/remove_all_pizzas', methods=['POST'])
@login_required
def remove_all_pizza():      
    #clear DB cart                                    
    userCart = Cart.query.filter_by(user_id=current_user.id).first() 
    if userCart:                                                                       
        userCart.content = ""
        db.session.commit()
    return render_template("cart.html", user=current_user, pizza = userCart.content)  

@views.route('/start_order', methods=['POST'])
@login_required
def start_order():
    chosen_id = request.form.get('chosen_id') 
    startedOrder = Order.query.get(chosen_id)       # Retrieve the order
    
    if startedOrder:                         # Check if the order exists
        startedOrder.status = "cooking"      # Update the status field    
        db.session.commit()                  # Commit the changes to the database


    return render_template("receiveOrders.html", user=current_user, order=order)  