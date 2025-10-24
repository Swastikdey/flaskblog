
from flask import render_template, url_for, flash,redirect, request,current_app,Blueprint
#current_app for finding out the root directory of my flask application
from my_app.users.forms import (RegistrationForm,LoginForm, UpdateForm,
                          RequestResetPasswordForm,
                          ResetPasswordForm )
from my_app import db,bcrypt
from flask_login import login_user, current_user, logout_user,login_required
from my_app.models import User, Post
import os
from my_app.users.utils import save_picture,send_reset_mail


users=Blueprint('users',__name__)


@users.route('/register',methods=['get','post'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm() # form is the instance of RegistrationForm class which we created
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #flash message
        flash(f"Your account has been created! You can now Log In", "success") #category here is success
        return redirect(url_for('users.login')) #home is the route function name
    return render_template('register.html', title='Register', form=form)

@users.route('/login',methods=['get','post'])
def login():
    if current_user.is_authenticated:#logged in already
        return redirect(url_for('main.home'))
    form=LoginForm()# form is the instance of LoginForm class which we created
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if not user:
            form.email.errors.append("Email is not registered with us.")
            #flash(f"Email is not registered with us. Sign Up?",'danger')
        elif user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
         
        
        else:
            flash(f"Can't Log in. Check username and password",'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route('/account',methods=['get','post'])
@login_required
def account():
    image_file=url_for( 'static', filename = "profile_pics/"+current_user.image_file ) 
    page=request.args.get('page', 1, type=int)
    posts=Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    form=UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
            if os.path.exists(image_path) and current_user.image_file!='default.jpg' :
                os.remove(image_path)  # Delete the file

            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file #update on db

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    return render_template('account.html',title='Account', image_file=image_file, form=form, posts=posts, user=current_user )



@users.route('/user/<string:username>',methods=['get','post'])
def user_posts(username): #user's profile page
    page=request.args.get('page', 1, type=int)
    user=User.query.filter_by(username=username).first_or_404()
    image_file=url_for( 'static', filename = "profile_pics/"+user.image_file ) 
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5, page=page)
    return render_template('user_posts.html', posts=posts, user=user,image_file=image_file)


@users.route('/reset_password',methods=['get','post'])
def reset_request():
    if current_user.is_authenticated:#logged in already
        return redirect(url_for('main.home'))
    form=RequestResetPasswordForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash(f"An Email has been sent to {form.email.data}, with instructions to reset password", 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password', form=form)

@users.route('/reset_password/<token>',methods=['get','post'])
def reset_token(token):
    if current_user.is_authenticated:#logged in already
        return redirect(url_for('main.home'))
    user_id=User.verify_reset_token(token)
    if user_id is None:
        flash('This is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    user=User.query.get(user_id)
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        #flash message
        flash(f"Your Password has been updated! You can now Log In", "success") #category here is success
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

#follow/unfollow

@users.route("/follow/<int:user_id>", methods=['POST'])
@login_required
def follow(user_id):
    user_to_follow = User.query.get_or_404(user_id)
    if user_to_follow == current_user:
        flash("You cannot follow yourself.", "warning")
        return redirect(url_for('users.user_profile', username=user_to_follow.username))
    
    if user_to_follow in current_user.following:
        flash("You are already following this user.", "info")
    else:
        current_user.following.append(user_to_follow)
        db.session.commit()
        flash(f"You are now following {user_to_follow.username}!", "success")
    
    return redirect(request.referrer or url_for('users.user_posts', username=user_to_follow.username))


@users.route("/unfollow/<int:user_id>", methods=['POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.get_or_404(user_id)
    if user_to_unfollow in current_user.following:
        current_user.following.remove(user_to_unfollow)
        db.session.commit()
        flash(f"You unfollowed {user_to_unfollow.username}.", "info")
    else:
        flash("You are not following this user.", "warning")
    
    return redirect(request.referrer or url_for('users.user_posts', username=user_to_unfollow.username))
