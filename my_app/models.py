from datetime import datetime,timezone
from my_app import db,login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

#current_app.app_context().push()
#db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(200), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)
    posts=db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    
    def get_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=None)
        token = s.dumps({'user_id':self.id})
        return token
    
    @staticmethod
    def verify_reset_token(token,max_age=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], salt=None)
        try:
            user_id=s.loads(token, max_age=max_age)['user_id']
        except:
            return None
        return user_id #this returns the ID of the user, which is int (1,2,3,....)

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=lambda:datetime.now(tz=timezone.utc))
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

