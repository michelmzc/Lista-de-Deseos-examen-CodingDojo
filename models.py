from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#from app import db
from .app import db

from sqlalchemy import select

class BaseModel(db.Model):
    __abstract__ = True 
    def get(self):
        return self
    
    def get_id(self):
        return self.id    
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.Text, nullable=False)
    #lastname  = db.Column(db.Text, nullable=False)
    email     = db.Column(db.String(256), unique=True, nullable=True)
    password  = db.Column(db.Text, nullable=False)
    date      = db.Column(db.Date)

    wishlist = db.relationship('WishList', back_populates='user')
    items    = db.relationship('Item', back_populates='user')
    def __repr__(self):
        return f'<User {self.email}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    def get_wishlist(self):
        all_items = db.session.execute(db.select(Item)).scalars()
        all_items_list = []
        for item in all_items:
            all_items_list.append(item)

        wishlists = db.session.execute(db.select(WishList).filter_by(user_id=self.id)).scalars()
        wishlist = []
        wishlist_items = []
        for wish in wishlists:
            wishlist.append(wish)
            wishlist_items.append(wish.item)
        
        other_wish = set(all_items_list) - set(wishlist_items)

        return wishlist, other_wish

class WishList(BaseModel):
    __tablename__= 'wishlists'
    id      = db.Column(db.Integer, primary_key=True)
    #date    = db.Column(db.Date)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', back_populates='wishlist')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id', ondelete='CASCADE'))
    item = db.relationship('Item', back_populates='wishlist')

    @staticmethod
    def get_by_id(id):
        wish = db.session.execute(db.select(WishList).filter_by(id=id)).scalar_one()
        return wish


class Item(BaseModel):
    __tablename__= 'items'
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.Text)
    date    = db.Column(db.Date)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', back_populates='items')

    wishlist = db.relationship('WishList', back_populates='item')

    @staticmethod 
    def remove(item_id):        
        wishs = db.session.execute(db.select(WishList).filter_by(item_id=item_id)).scalars()
        for wish in wishs:
            wish.delete()
        item = db.session.execute(db.select(Item).filter_by(id=item_id)).scalar_one()
        item.delete()
    
    @staticmethod 
    def get_by_id(item_id):                
        item = db.session.execute(db.select(Item).filter_by(id=item_id)).scalar_one()

        wishs = db.session.execute(db.select(WishList).filter_by(item_id=item_id)).scalars()
        user_wishlist = []
        for wish in wishs:
            user_wishlist.append(wish.user.name)

        return item, user_wishlist
        


