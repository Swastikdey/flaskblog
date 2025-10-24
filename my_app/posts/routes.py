
from flask import render_template, url_for, flash,redirect, request,abort,Blueprint
from my_app.posts.forms import (PostForm )
from my_app import db
from flask_login import current_user, login_required
from my_app.models import Post, Comment
 


posts=Blueprint('posts',__name__)




@posts.route('/post/new',methods=['get','post'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post is created!",'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form,legend="New Post")

@posts.route('/post/<int:post_id>', methods=['get'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    comments = post.comments.order_by(Comment.date_posted.desc()).all()
    return render_template('post.html',title=post.title, post=post, comments=comments )

@posts.route('/post/<int:post_id>/update' ,methods=['get','post'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()# no need to add, since we are just updating
        flash("Post has been updated",'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    #please explain this elif part
    return render_template('create_post.html', title='Update Post',
                           form=form,legend="Update Post")

@posts.route('/post/<int:post_id>/delete' ,methods=['post'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("your post has been deleted.", 'success')
    return redirect(url_for('main.home'))

#like and comments

@posts.route("/like/<int:post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    if post in current_user.liked_posts:
        current_user.liked_posts.remove(post)
        flash("You unliked the post.", "info")
    else:
        current_user.liked_posts.append(post)
        flash("You liked the post!", "success")
    
    db.session.commit()
    return redirect(request.referrer or url_for('posts.post', post_id=post.id))


@posts.route("/comment/<int:post_id>", methods=['POST'])
@login_required
def add_comment(post_id):
    content = request.form.get("content")
    if not content.strip():
        flash("Comment cannot be empty.", "warning")
        return redirect(request.referrer or url_for('posts.post', post_id=post_id))

    new_comment = Comment(content=content, user_id=current_user.id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    flash("Comment added!", "success")
    return redirect(request.referrer or url_for('posts.post', post_id=post_id))

@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id and comment.post.author != current_user:
        flash("You cannot delete this comment.", "danger")
        return redirect(request.referrer or url_for('posts.post', post_id=comment.post_id))
    
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "info")
    return redirect(request.referrer or url_for('posts.post', post_id=comment.post_id))
