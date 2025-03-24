from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'

# Admin configuration
ADMIN_PASSWORD = "admin123"
orders = []

# Load existing orders
if os.path.exists('orders.json'):
    with open('orders.json', 'r') as f:
        orders = json.load(f)

# Menu configuration
menu = {
    'cheeseburger': {'name': 'Cheeseburger', 'price': 15000},
    'cheese_sandwich': {'name': 'Cheese Sandwich', 'price': 18000},
    'chicken_burgers': {'name': 'Chicken Burgers', 'price': 25000},
    'spicy_chicken': {'name': 'Spicy Chicken', 'price': 22000},
    'hot_dog': {'name': 'Hot Dog', 'price': 10000},
    'fruit_salad': {'name': 'Fruit Salad', 'price': 8000},
    'cocktails': {'name': 'Cocktails', 'price': 18000},
    'nuggets': {'name': 'Nuggets', 'price': 9000},
    'sandwich': {'name': 'Sandwich', 'price': 16000},
    'french_fries': {'name': 'French Fries', 'price': 7000},
    'milk_shake': {'name': 'Milk Shake', 'price': 3000},
    'iced_tea': {'name': 'Iced Tea', 'price': 2000},
    'orange_juice': {'name': 'Orange Juice', 'price': 2500},
    'lemon_tea': {'name': 'Lemon Tea', 'price': 1500}
}

def save_orders():
    with open("orders.json", "w") as f:
        json.dump(orders, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html', menu=menu)

@app.route('/order-approval', methods=['POST'])
def order_approval():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        location = request.form['location']
        selected_items = request.form.getlist('order')
        
        order_details = []
        total_price = 0
        
        for item_key in selected_items:
            if item_key in menu:
                item = menu[item_key]
                order_details.append({
                    'name': item['name'],
                    'price': item['price']
                })
                total_price += item['price']

        session['pre_order'] = {
            'customer_name': customer_name,
            'location': location,
            'items': order_details,
            'total_price': total_price
        }

        return render_template('order_approval.html',
                             order=order_details,
                             total_price=total_price,
                             customer_name=customer_name,
                             location=location)

@app.route('/submit-order', methods=['POST'])
def submit_order():
    if 'pre_order' not in session:
        return redirect(url_for('index'))
    
    final_order = session['pre_order']
    
    new_order = {
        'order_id': len(orders) + 1,
        'customer_name': final_order['customer_name'],
        'location': final_order['location'],
        'items': final_order['items'],
        'total_price': final_order['total_price'],
        'status': 'Pending',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    orders.append(new_order)
    save_orders()
    
    session['order'] = new_order
    session.pop('pre_order', None)
    
    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    order = session.get('order')
    if not order:
        flash("No order found", "error")
        return redirect(url_for('index'))
        
    return render_template('confirmation.html', order=order)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return render_template('admin_dashboard.html', orders=orders)
        else:
            flash("Wrong password", "error")
    
    if session.get('admin_logged_in'):
        return render_template('admin_dashboard.html', orders=orders)
    
    return render_template('admin_login.html')

@app.route('/update-status/<int:order_id>/<new_status>')
def update_status(order_id, new_status):
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin'))
    
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = new_status
            save_orders()
            break
            
    return redirect(url_for('admin'))

@app.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)