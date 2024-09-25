from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import BooleanField,StringField,PasswordField,FileField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Beni Hatırla')
    submit = SubmitField('Log in')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email =StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sing Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError("Bu Kullanıcı Adı Kullanılmaktadır!")
        
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Bu Email Kullanılmaktadır!")

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("Bu kullanıcı adı kullanılıyor")

    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Bu Email Kullanılmaktadır") 
            
class RoleUser(FlaskForm):
    role = SelectField('role',choices=["admin","user"],validate_choice=True)