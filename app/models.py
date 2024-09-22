from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.description}', {self.price})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("orders", lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product", backref=db.backref("orders", lazy=True))
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Order('{self.user.username}', '{self.product.name}')"
    
    #Product Catalog
    from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Product('{self.name}', '{self.description}', {self.price}, '{self.category}')"
    
    from app import db

class Product(db.Model):
    # ... (existing code)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("Product", backref="cart_items")
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"CartItem('{self.product.name}', {self.quantity})"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cart_items = db.relationship("CartItem", backref="order")

    def __repr__(self):
        return f"Order('{self.customer_name}', '{self.customer_email}', {self.order_date})"
    
    from app import db

class Order(db.Model):
    # ... (existing code)

    status = db.Column(db.String(50), nullable=False, default="pending")
    tracking_number = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Order('{self.customer_name}', '{self.customer_email}', {self.order_date}, {self.status})"