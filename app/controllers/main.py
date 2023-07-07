from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import NoResultFound
from app.extensions import cache, limiter, csrf
from app.forms import LoginForm, SignInForm
from app.models import User, Post, db
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.post('/realtime')
@csrf.exempt
def real_time_posts():
    query = db.session.query(Post).join(User).options(joinedload(Post.user)).order_by(desc(Post.created_at))
    # Fetch the results
    results = query.all()
    # Convert results to JSON
    json_results = [{'post_id': post.id, 'content': post.content, "created_at": post.created_at, 'user_id': post.user.id, 'user_name': post.user.username} for post in results]
    return jsonify(json_results)

@main.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per day')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).one()
            login_user(user)

            flash('Logged in successfully')
        except NoResultFound:
            flash("Username doesn't exists")
            return redirect(url_for('main.login'))
        return redirect(request.args.get('next') or url_for('.home'))

    return render_template('login.html', form=form)

@main.route('/signin', methods=['GET', 'POST'])
@limiter.limit('5 per day')
def signin():
    form  = SignInForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=generate_password_hash(form.password.data))
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('You have Signed in successfully!')
            return redirect(url_for('main.home'))
        except Exception as e:
            flash(f'An Error occurd: {str(e)}')
            return redirect(url_for('main.home'))
    return render_template("signin.html", form=form)
@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    
    return redirect(url_for('.home'))
