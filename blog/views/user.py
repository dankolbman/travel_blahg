from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_required, current_user

from blog.extensions import cache
from blog.models import db
from blog.forms import CreatePostForm
from blog.models import User, Post

user = Blueprint('user', __name__)

@user.route('/')
def home():
  return 'Hi user'

@user.route('/write', methods=['GET','POST'])
@login_required
def write():
  """ Write a new post page """
  form = CreatePostForm()
  
  if form.validate_on_submit():
    post = Post(author=current_user._get_current_object(),
              title=form.title.data,
              body=form.body.data)

    db.session.add(post)
    db.session.commit()

    print('NEW POST!!!')
    print(post.id)

    flash("You made a new post!")
    return redirect(url_for('.post', id=post.id))
  return render_template('new_post.html', form=form)

@user.route('/edit_profile')
@login_required
def edit_profile():
  return 'Editing profile'

@user.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
  p = Post.query.get_or_404(id)
  return render_template('post.html', post=p)

