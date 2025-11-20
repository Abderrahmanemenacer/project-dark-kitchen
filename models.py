import psycopg2
from extensions import db
import enum
from datetime import date, datetime

# ENUM for order status
class order_status_type(enum.Enum):
    pending = 'pending'
    in_progress = 'in progress'
    completed = 'completed'
    canceled = 'canceled'

# Address table
class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wilaya = db.Column(db.String(255))
    baladiya = db.Column(db.String(255))
    longitude = db.Column(db.Numeric(11, 8))
    latitude = db.Column(db.Numeric(10, 8))
    
    # Relationship: One Address can have multiple Users.
    users = db.relationship('User', back_populates='address')


# User table
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.Date, default=date.today, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    pfp = db.Column(db.String(255), nullable=False)

    address = db.relationship('Address', back_populates='users')
    kitchens = db.relationship('Kitchen', back_populates='user')
    favorites = db.relationship('Favorite', back_populates='user')
    phone_numbers = db.relationship('UserPhoneNumber', back_populates='user', cascade="all, delete-orphan")
    kitchen_reviews = db.relationship('KitchenReview', back_populates='user')
    item_reviews = db.relationship('ItemReview', back_populates='user')
    orders = db.relationship('Order', back_populates='user')
    cart = db.relationship('Cart', uselist=False, back_populates='user')

# Kitchen table
class Kitchen(db.Model):
    __tablename__ = 'kitchen'
    kitchen_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kitchen_name = db.Column(db.String(255), nullable=False)
    kitchen_bio = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    cvp = db.Column(db.String(255), nullable=False)
    avg_rating = db.Column(db.Float, nullable=False, default=0.0)
    
    user = db.relationship('User', back_populates='kitchens')
    items = db.relationship('Item', back_populates='kitchen', cascade="all, delete-orphan")
    reviews = db.relationship('KitchenReview', back_populates='kitchen')
    ads = db.relationship('Ad', back_populates='kitchen')


    def avgrating(self):
        if not self.reviews:
        # Keep the old avg_rating value, do NOT reset it to 0
            return self.avg_rating  
        else:
            self.avg_rating = sum([review.nbr_of_stars for review in self.reviews]) / len(self.reviews)
            db.session.commit()
        return self.avg_rating


# Category table
class Category(db.Model):
    __tablename__ = 'categories'
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(100), unique=True, nullable=False)
    
    items = db.relationship('Item', back_populates='item_category')


# Items table
class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    avg_rating = db.Column(db.Float, nullable=False, default=0.0)

    item_title = db.Column(db.String(255))
    item_description = db.Column(db.String(255))
    post_date = db.Column(db.Date)
    aavailability = db.Column(db.Boolean)
    price = db.Column(db.Float)

    cat_id = db.Column(db.Integer, db.ForeignKey('categories.cat_id'), nullable=True)

    kitchen_id = db.Column(db.Integer, db.ForeignKey('kitchen.kitchen_id'))
    
    kitchen = db.relationship('Kitchen', back_populates='items')
    item_category = db.relationship('Category', back_populates='items', foreign_keys=[cat_id])
    favorites = db.relationship('Favorite', back_populates='item')
    gallery = db.relationship('Gallery', back_populates='item', cascade="all, delete-orphan")
    reviews = db.relationship('ItemReview', back_populates='item', cascade="all, delete-orphan")
    cart_items = db.relationship('CartItem', back_populates='item')
    order_items = db.relationship('OrderItem', back_populates='item')
    def avgrating(self):
        if not self.reviews:
        # Keep the old avg_rating value, do NOT reset it to 0
            return self.avg_rating  
        else:
            self.avg_rating = sum([review.nbr_of_stars for review in self.reviews]) / len(self.reviews)
            db.session.commit()
        return self.avg_rating



# Favorites table
class Favorite(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), primary_key=True)
    
    user = db.relationship('User', back_populates='favorites')
    item = db.relationship('Item', back_populates='favorites')


# User phone numbers
class UserPhoneNumber(db.Model):
    __tablename__ = 'user_phone_number'
    phone_num_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    number = db.Column(db.String(20))
    user = db.relationship('User', back_populates='phone_numbers')


# Ads table
class Ad(db.Model):
    __tablename__ = 'ads'
    ads_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kitchen_id = db.Column(db.Integer, db.ForeignKey('kitchen.kitchen_id'), nullable=False)
    image_link = db.Column(db.String(255))
    
    kitchen = db.relationship('Kitchen', back_populates='ads')


# Kitchen reviews table
class KitchenReview(db.Model):
    __tablename__ = 'kitchen_reviews'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    kitchen_id = db.Column(db.Integer, db.ForeignKey('kitchen.kitchen_id'), primary_key=True)

    review_body = db.Column(db.Text)
    nbr_of_stars = db.Column(db.Float, nullable=False)
    
    user = db.relationship('User', back_populates='kitchen_reviews')
    kitchen = db.relationship('Kitchen', back_populates='reviews')


# Gallery table
class Gallery(db.Model):
    __tablename__ = 'gallery'
    img_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_link = db.Column(db.String(255))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id', ondelete='CASCADE'))
    
    item = db.relationship('Item', back_populates='gallery')


# Item reviews table
class ItemReview(db.Model):
    __tablename__ = 'item_reviews'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id', ondelete='CASCADE'), primary_key=True)

    review_body = db.Column(db.String(255) , nullable=False)
    nbr_of_stars = db.Column(db.Float  , nullable=False)
    
    user = db.relationship('User', back_populates='item_reviews')
    item = db.relationship('Item', back_populates='reviews')


# Order table
class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    order_date = db.Column(db.Date, default=lambda: date.today())

    total_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.user_id') , nullable = False)
    order_status = db.Column(db.Enum(order_status_type), nullable=False)

    
    user = db.relationship('User', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')


# Cart table
class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True , autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    
    user = db.relationship('User', back_populates='cart')
    cart_items = db.relationship('CartItem', back_populates='cart',cascade="all, delete-orphan")


# CartItem table
class CartItem(db.Model):
    __tablename__ = 'cart_item'
    cart_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cart_id = db.Column(db.Integer,db.ForeignKey('cart.cart_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False, default=1)
    note = db.Column(db.String(1024), nullable=True)
    
    cart = db.relationship('Cart', back_populates='cart_items')
    item = db.relationship('Item', back_populates='cart_items')


# OrderItem table
class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_item_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    
    note = db.Column(db.String(1024))
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order_time = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', back_populates='order_items')
    item = db.relationship('Item', back_populates='order_items')