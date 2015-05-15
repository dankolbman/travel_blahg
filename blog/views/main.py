from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from blog.extensions import cache
from blog.forms import LoginForm
from blog.models import User, Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
  """ Home page """
  # Show recent posts
  p = Post.query.limit(5).all()
  return render_template('index.html', posts=p)

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
