from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms import CreatePostForm
from app.extensions import csrf
from flask_login import login_required, current_user
from app.models import Post, db

blog_post = Blueprint('post', __name__)

@blog_post.route('/post', methods=['POST', 'GET'])
@login_required
@csrf.exempt
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
                content=form.data.get('content'),
                user_id= current_user.id,
            )
        try:
            db.session.add(post)
            db.session.commit()
            flash("Your post has been added succesfully!")
            return redirect(url_for('main.home'))
        except Exception as e:
            db.session.rollback()
            flash("Something went wrong while saving your post please try again")
            return redirect(url_for('post.create_post'))
        
            
    return render_template('create_post.html', form=form)
