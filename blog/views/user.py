import os, random, string

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_file
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename 

from blog.extensions import cache
from blog.models import db
from blog.forms import CreatePostForm, CreateImageForm
from blog.models import User, Post, TextPost, ImagePost

user = Blueprint('user', __name__)

@user.route('/')
def home():
  return 'Hi user'

@user.route('/image/<path:path>', methods=['GET'])
def prox(path):
  path = os.path.join(current_app.config['UPLOAD_FOLDER'], path)
  return send_file(path)

@user.route('/new_text', methods=['GET','POST'])
@login_required
def new_text():
  """ Write a new text post page """
  form = CreatePostForm()
  
  if form.validate_on_submit():
    textpost = TextPost(author=current_user._get_current_object(),
              title=form.title.data,
              text=form.text.data,
              latitude=form.latitude.data,
              longitude=form.longitude.data)

    db.session.add(textpost)
    db.session.commit()

    flash("You made a new post!")
    return redirect(url_for('.post', id=textpost.id))
  return render_template('new_text.html', form=form)

@user.route('/new_image', methods=['GET','POST'])
@login_required
def new_image():
  """ Make a new image post by uploading a file """
  form = CreateImageForm()

  if request.method == 'POST':
    f = request.files['image']
    if f and allowed_file(f.filename):
      filename = secure_filename(f.filename)
      filename = os.path.splitext(filename)[1]
      rname = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
      filename = rname+filename
      fpath = os.path.join('blog',current_app.config['UPLOAD_FOLDER'], filename)
      f.save(fpath)

      imagepost = ImagePost(author=current_user._get_current_object(),
                    title=form.title.data,
                    caption=form.caption.data,
                    image_path=filename,
                    latitude=form.latitude.data,
                    longitude=form.longitude.data)

      db.session.add(imagepost)
      db.session.commit()
      return redirect(url_for('.post', id=imagepost.id))
  return render_template('new_image.html', form=form)

@user.route('/edit_profile')
@login_required
def edit_profile():
  return 'Editing profile'

@user.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
  p = Post.query.get_or_404(id)
  return render_template('post.html', post=p)

def allowed_file(filename):
  """ Helper function to determine what files are allowed """
  return ('.' in filename and \
    filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS'])

