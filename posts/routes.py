from flask import Blueprint , render_template , redirect , url_for , request
from flask_login import login_required , login_user , current_user , logout_user
from posts.forms import CreatePost, CreateCategory
from config import db
from models import Category , Post , Comment

posts = Blueprint('posts',__name__)

@posts.route("/createpost", methods=['GET','POST'])
@login_required
def createpost():
    form = CreatePost()
    form.category.choices = [(category.id , category.category_name) for category in Category.query.all()]
    if form.validate_on_submit():
        post = Post(title = form.title.data ,content = form.content.data, user_id = current_user.id, category_id = form.category.data )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("createpost.html", title ="Create Post", form = form , category = Category.query.all())

@posts.route("/createcategory",methods = ['GET','POST'])
@login_required
def createcategory():
    form = CreateCategory()
    if form.validate_on_submit():
        category = Category(category_name = form.category_name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template("createcategory.html", title = "Create Category" , form = form ,category= Category.query.all())

@posts.route("/deletepost/<int:id>")
@login_required
def deletepost(id):
    Post.query.filter_by(id=123).delete()
    return redirect(url_for("main.index"))

@posts.route("/postdetailed/<int:id>",methods=['GET','POST'])
def postdetailed( id ):
    print(id)
    post = Post.query.filter_by(id = id).first()
    print("---",post)
    comment = Comment.query.filter_by( post_id = id )
    return render_template("postDetailed.html", post = post , comment = comment, category=Category.query.all())

@posts.route("/addcomment/<int:id>" , methods=['GET','POST'])
@login_required
def addcomment(id):
    print(request.form.get('content'))
    commit = Comment(content = request.form.get('content') , post_id = id , username = current_user.username)
    db.session.add(commit)
    db.session.commit()
    return redirect(url_for("posts.postdetailed",id=id))

@posts.route("/categorylist/<int:id>")
def categorylist(id):
    post = Post.query.filter_by(category_id=id)
    name = Category.query.filter_by(id=id).first().category_name
    return render_template("category.html",title= name + "Post" ,post = post, category=Category.query.all())
