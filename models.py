from datetime import datetime
from config import db,login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))
   
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    image_file = db.Column(db.String(60),nullable=False,default="static/img/default.jpg")
    description = db.Column(db.String(60))
    create_date = db.Column(db.Date,nullable=False,default = datetime.now)
    role_name = db.Column(db.String(20),nullable = False,default = 'user')

class Post(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(20),nullable = False)
    content = db.Column(db.String(200),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable = False)
    create_date = db.Column(db.Date,nullable=False,default = datetime.now)

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    username = db.Column(db.String,db.ForeignKey('user.username'),nullable=False)
    content = db.Column(db.String(100),nullable=False)
    create_date = db.Column(db.Date,nullable=False,default = datetime.now)

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(20),nullable=False)