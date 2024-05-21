from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
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