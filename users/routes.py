from flask import Flask ,Blueprint,render_template,current_app,url_for,flash,redirect,request
from flask_login import login_required, login_user, current_user, logout_user
from users.forms import LoginForm, RegisterForm, UpdateAccountForm , RoleUser
from config import db,bcrypt
from models import User , Category 
import secrets,os
from PIL import Image
from datetime import datetime

users = Blueprint('users',__name__)

@users.route("/login" , methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            flash('Giriş Yapıldı',"success")
            return redirect(url_for('main.index'))
        else:
            flash('Giriş Başarısız','danger')
    return render_template('login.html' ,title="Login",form = form , category= Category.query.all())

@users.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data,password = hashed_password)
        db.session.add( user )
        db.session.commit()
        flash("Kayıt Başarılı")
        return redirect(url_for('users.login'))
    return render_template("register.html",title="Register",form = form , category= Category.query.all())

@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash(" Profil Güncellendi! Profil Resmi eklendi ")
        return redirect(url_for('users.account'))
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile/'+ current_user.image_file)
    return render_template('account.html',title="Account", image_file = image_file , form = form , category= Category.query.all())

@users.route("/user" , methods=['GET','POST'])
@login_required
def user():
    user = User.query.all()
    return render_template("users.html" , title = "Users", user = user, category= Category.query.all())

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static','profile',picture_filename)
    print(picture_path)

    output_size=(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename

