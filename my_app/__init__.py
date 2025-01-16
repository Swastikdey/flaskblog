from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from my_app.config import Config


mail=Mail()
db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category='info'



def create_app(config_class=Config):
    app=Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from my_app.users.routes import users
    from my_app.posts.routes import posts
    from my_app.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app