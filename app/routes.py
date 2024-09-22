from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid username or password")
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product.html", product=product)

@app.route("/cart")
@login_required
def cart():
    # TO DO: implement cart functionality
    return render_template("cart.html")

@app.route("/checkout")
@login_required
def checkout():
    # TO DO: implement checkout functionality
    return render_template("checkout.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, UserMixin

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid username or password")
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

from flask import render_template, request
from app import app, db
from app.models import Product

@app.route("/products", methods=["GET"])
def products():
    products = Product.query.all()
    return render_template("products.html", products=products)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    products = Product.query.filter((Product.name.like("%" + query + "%")) | (Product.description.like("%" + query + "%"))).all()
    return render_template("products.html", products=products)

@app.route("/filter", methods=["GET"])
def filter():
    category = request.args.get("category")
    products = Product.query.filter_by(category=category).all()
    return render_template("products.html", products=products)

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Product, CartItem, Order

# ... (existing code)

@app.route("/cart", methods=["GET"])
def cart():
    cart_items = CartItem.query.all()
    return render_template("cart.html", cart_items=cart_items)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])
    cart_item = CartItem(product_id=product_id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        customer_name = request.form["customer_name"]
        customer_email = request.form["customer_email"]
        order = Order(customer_name=customer_name, customer_email=customer_email)
        db.session.add(order)
        db.session.commit()
        cart_items = CartItem.query.all()
        for cart_item in cart_items:
            order.cart_items.append(cart_item)
        db.session.commit()
        return redirect(url_for("order_confirmation"))
    return render_template("checkout.html")

@app.route("/order_confirmation", methods=["GET"])
def order_confirmation():
    return render_template("order_confirmation.html")

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Product, CartItem, Order
import stripe

stripe.api_key = app.config["PAYMENT_GATEWAY_API_KEY"]
stripe.secret_key = app.config["PAYMENT_GATEWAY_SECRET_KEY"]

# ... (existing code)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        customer_name = request.form["customer_name"]
        customer_email = request.form["customer_email"]
        order = Order(customer_name=customer_name, customer_email=customer_email)
        db.session.add(order)
        db.session.commit()
        cart_items = CartItem.query.all()
        for cart_item in cart_items:
            order.cart_items.append(cart_item)
        db.session.commit()
        
        # Create a Stripe payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.total_price * 100),  # Convert to cents
            currency="usd",
            payment_method_types=["card"]
        )
        
        # Redirect to Stripe payment page
        return redirect(url_for("payment", payment_intent_id=payment_intent.id))
    
    return render_template("checkout.html")

@app.route("/payment/<payment_intent_id>", methods=["GET"])
def payment(payment_intent_id):
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    return render_template("payment.html", payment_intent=payment_intent)

@app.route("/payment_success", methods=["GET"])
def payment_success():
    return render_template("payment_success.html")

@app.route("/payment_failure", methods=["GET"])
def payment_failure():
    return render_template("payment_failure.html")

from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Product, CartItem, Order

# ... (existing code)

@app.route("/order_management", methods=["GET"])
def order_management():
    orders = Order.query.all()
    return render_template("order_management.html", orders=orders)

@app.route("/update_order_status", methods=["POST"])
def update_order_status():
    order_id = request.form["order_id"]
    status = request.form["status"]
    order = Order.query.get(order_id)
    order.status = status
    db.session.commit()
    return redirect(url_for("order_management"))

@app.route("/track_order", methods=["GET"])
def track_order():
    order_id = request.args.get("order_id")
    order = Order.query.get(order_id)
    return render_template("track_order.html", order=order)