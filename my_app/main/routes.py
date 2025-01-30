from flask import render_template, request,Blueprint
from my_app.models import Post
 


main=Blueprint('main',__name__)




@main.route('/home')
def home():
    page=request.args.get('page', 1, type=int)
    myposts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('home.html',posts=myposts)

@main.route('/about')
def about():
    print("Title passed to template:", "about")  # Debug line
    return render_template('about.html',title="About3")

