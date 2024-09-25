from wtforms import StringField,TextAreaField,SelectField,SubmitField
from wtforms.validators import DataRequired ,ValidationError
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea
from models import Category

class CreatePost(FlaskForm):
    title = StringField("Post Title",validators=[DataRequired()])
    content = TextAreaField('Content', widget=TextArea())
    category = SelectField('Category',choices=[],validate_choice=True)

class CreateCategory(FlaskForm):
    category_name = StringField('Category',validators=[DataRequired()])
    submit = SubmitField("Add")
    

    def validate_category(self,category_name):
        category_name = Category.query.filter_by(category_name=category_name.data).first()
        if category_name:
            raise ValidationError("Böyle bir Kategory Mevcut")