from flask import Flask, render_template, request

app = Flask(__name__)

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
        
        # Display the details on the confirmation page
        return render_template('confirmation.html', 
                               order=order, 
                               total_price=total_price,
                               customer_name=customer_name,
                               location=location)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
