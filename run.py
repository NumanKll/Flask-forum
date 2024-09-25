from flask import Flask
from config import Config, db , bcrypt , login_manager

app =Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

from users.routes import users
from posts.routes import  posts
from home.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)