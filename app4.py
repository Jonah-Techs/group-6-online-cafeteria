from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# In-memory storage for orders (will reset if server restarts)
orders = []

# Route to display the menu and capture order details
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Capture Order Details
        order = request.form.getlist('order')
        total_price = request.form.get('total_price')

        # Capture Customer Details
        customer_name = request.form.get('customer_name')
        location = request.form.get('location')
        
        # Save the order to the in-memory list
        orders.append({
            'customer_name': customer_name,
            'location': location,
            'order': order,
            'total_price': total_price
        })

        # Redirect to confirmation page
        return render_template('confirmation.html', 
                               order=order, 
                               total_price=total_price,
                               customer_name=customer_name,
                               location=location)
    return render_template('index.html')

# Route to display all orders on an Admin Dashboard
@app.route('/admin')
def admin():
    return render_template('admin.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
