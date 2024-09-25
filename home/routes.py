from flask import Blueprint , render_template
from models import Post , Category

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/index")
def index():
    post = Post.query.all()
    return render_template("index.html",title = "Home",post = post , category= Category.query.all())