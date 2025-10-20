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

likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

#association table 
followers = db.Table( 
    'followers',
    db.Column('the_follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('the_followed_id', db.Integer, db.ForeignKey('user.id'))
)
#   It’s not a model class (like User), but a plain association table —
#   used to connect users to other users in a many-to-many relationship.

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file=db.Column(db.String(200), nullable=False, default='default.jpg')
    password=db.Column(db.String(60), nullable=False)

    posts=db.relationship('Post',
                          backref='author',
                          lazy=True,
                          cascade='all, delete-orphan'
                        )
#   this line doesn’t create a column in the database.
#   Instead, it creates a Python attribute (user.posts) that gives you all related Post objects.
    
    following = db.relationship( #manages the follower/following
        'User', secondary=followers,
        primaryjoin=(followers.c.the_follower_id == id),
        secondaryjoin=(followers.c.the_followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
    #user.following.all() gives the followings
    #user.followers.all() gives the followers of user

    liked_posts = db.relationship('Post', 
        secondary=likes,
        backref=db.backref('liked_by', lazy='dynamic'), #in reverse relationship also, lazy=dynamic is applied
        lazy='dynamic' 
    )   
    # user.liked_posts.all() gives all the posts that the user liked
    # post.liked_by.all() gives all the users eho liked the post
    # lazy='dynamic'gives you a query object instead of a list. 
    # user.liked_posts.filter_by(title='Test Post').all()
    # user.liked_posts.count()

    comments = db.relationship(
        'Comment',
        backref='user', # backref=db.backref('user', lazy='dynamic') is avoided here, quereability is not required
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

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

    comments = db.relationship(
        'Comment',
        backref='post',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(tz=timezone.utc))

    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id=db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"<Comment by User {self.user_id} on Post {self.post_id}>"

