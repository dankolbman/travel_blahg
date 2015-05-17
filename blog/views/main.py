from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app
from flask.ext.login import login_user, logout_user, login_required

from blog.extensions import cache
from blog.models import db
from blog.forms import LoginForm, NewUserForm
from blog.models import User, Post

import os
main = Blueprint('main', __name__)

@main.route('/')
@cache.cached(timeout=60)
def index():
  """ Home page """
  # Show recent posts and paginate
  page = request.args.get('page', 1, type=int)
  pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
    page, per_page=10, error_out=False)
  posts = pagination.items

  return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/register', methods=["GET", "POST"])
@cache.cached(timeout=300)
def new_user():
  """ Sign up a new user """
  form = NewUserForm()

  if form.validate_on_submit():
    user = User(email=form.email.data,
                username=form.username.data,
                password=form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Welcome to {0}!'.format(current_app.config['APP_NAME']))
    return redirect(url_for('.login'))
  return render_template('register.html', form=form)

  

@main.route("/login", methods=["GET", "POST"])
def login():
  """ Login page, shows the login form """
  form = LoginForm()

  if form.validate_on_submit():
      user = User.query.filter_by(username=form.username.data).one()
      login_user(user)

      flash("You've been logged in.", "success")
      return redirect(url_for(".index"))

  return render_template("login.html", form=form)

@main.route('/logout')
def logout():
  logout_user()
  flash("You were logged out", "success")

  return redirect(url_for(".index"))
