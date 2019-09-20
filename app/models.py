from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    
    def __repr__(self):
      return f'User {self.username}'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
    
    
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer,primary_key = True)
    cat_name = db.Column(db.String(255))


    def __repr__(self):
        return f'User {self.cat_name}'    

class Pitch(db.Model):

    __tablename__ = 'pitch'

    id = db.Column(db.Integer,primary_key = True)
    pitch_title = db.Column(db.String)
    your_pitch = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    category_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    users = db.relationship('User',backref = 'role',lazy="dynamic")
    category = db.relationship('Category',backref = 'role',lazy="dynamic") 
       
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_pitch(cls,id):
        pitch = Pitch.query.filter_by(category_id=id).all()
        return pitch
    
        




