import os, random, string

from datetime import datetime

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_file
from flask.ext.login import login_required, current_user
from werkzeug import secure_filename 

from sqlalchemy import desc
from geoalchemy2 import Geometry

from blog.extensions import cache
from blog.models import db
from blog.forms import CreatePostForm, CreateImageForm, EditProfileForm
from blog.models import User, Post, TextPost, ImagePost, Ping

user = Blueprint('user', __name__)

@user.route('/')
def home():
  p = Post.query.filter_by(author_id=current_user.id).order_by(desc(Post.timestamp)).limit(10).all()
  return render_template('index.html', posts=p, user=current_user)

@user.route('/<path:username>')
def user_page(username):
  user =  User.query.filter_by(username=username).first()
  if user != None:
    p = Post.query.filter_by(author_id=user.id).order_by(desc(Post.timestamp)).limit(10).all()
    return render_template('index.html', posts=p, user=user)
  else:
    return 'Couldn\'t find user {0}'.format(username)

@user.route('/image/<path:path>', methods=['GET'])
def prox(path):
  path = os.path.join(current_app.config['UPLOAD_FOLDER'], path)
  return send_file(path)

@user.route('/pings')
def ping_map():
  """ Show a map with users pings """
  import json
  pings = Ping.query.filter_by(author_id=current_user.id).order_by(desc(Ping.timestamp)).limit(10).all()

  geo_json = []
  for ping in pings:
    geom = json.loads(db.session.scalar(ping.loc.ST_AsGeoJSON()))
    geo_json.append({"type":"Feature",'geometry':geom})

  geo_json = json.dumps(geo_json)

  return render_template('user/ping_map.html', pings = pings, geo_json=geo_json)


@user.route('/text', methods=['GET','POST'])
@login_required
def new_text():
  """ Write a new text post page """
  form = CreatePostForm()
  
  if form.validate_on_submit():
    t = datetime.utcnow()
    textpost = TextPost(author=current_user._get_current_object(),
              title=form.title.data,
              timestamp=t,
              text=form.text.data,
              latitude=form.latitude.data,
              longitude=form.longitude.data,
              loc='POINT({0} {1})'.format(form.longitude.data,form.latitude.data))
    ping = Ping(author=current_user._get_current_object(),
                timestamp=t,
                loc='POINT({0} {1})'.format(form.longitude.data,form.latitude.data))

    db.session.add(textpost)
    db.session.add(ping)
    db.session.commit()

    flash("You made a new post!")
    return redirect(url_for('.post', id=textpost.id))
  return render_template('user/text.html', form=form)

@user.route('/image', methods=['GET','POST'])
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

      t = datetime.utcnow()
      imagepost = ImagePost(author=current_user._get_current_object(),
                    title=form.title.data,
                    timestamp=t,
                    caption=form.caption.data,
                    image_path=filename,
                    latitude=form.latitude.data,
                    longitude=form.longitude.data,
                    loc='POINT({0} {1})'.format(form.longitude.data,form.latitude.data))
      ping = Ping(author=current_user._get_current_object(),
                    timestamp=t,
                    loc='POINT({0} {1})'.format(form.longitude.data,form.latitude.data))


      db.session.add(imagepost)
      db.session.add(ping)
      db.session.commit()
      return redirect(url_for('.post', id=imagepost.id))
  return render_template('user/image.html', form=form)

@user.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_post(id):
  """ Edit a post """
  p = Post.query.get(id)
  if p.author_id != current_user.id:
    return 'This isn\'t your post!!!'
  else:
    ### Text post
    if isinstance(p, TextPost):
      form = CreatePostForm(title=p.title,
                            text=p.text,
                            latitude=p.latitude,
                            longitude=p.longitude)

      if form.validate_on_submit():
        p.title=form.title.data
        p.text=form.text.data
        p.latitude=form.latitude.data
        p.longitude=form.longitude.data
        db.session.commit()
        return redirect(url_for('.post', id=p.id))
      return render_template('user/text.html', form=form, pid=p.id)
    ### Image post
    if isinstance(p, ImagePost):
      form = CreateImageForm(title=p.title,
                            caption=p.caption,
                            latitude=p.latitude,
                            longitude=p.longitude)

      if form.validate_on_submit():
        p.title=form.title.data
        p.text=form.caption.data
        p.latitude=form.latitude.data
        p.longitude=form.longitude.data
        p.loc = 'POINT({0} {1})'.format(form.longitude.data,form.latitude.data)
        db.session.commit()
        return redirect(url_for('.post', id=p.id))
      return render_template('user/image.html', form=form, pid=p.id)

@user.route('/delete/<int:id>')
@login_required
def delete_post(id):
  """ Delete a post """
  p = Post.query.get(id)
  if p.author_id != current_user.id:
    return 'This isn\'t your post!!!'
  else:
    flash('"{0}" was deleted'.format(p.title))
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('main.index'))
  

@user.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
  form = EditProfileForm(username=current_user.username,\
                         email=current_user.email,\
                         api_key=current_user.api_key)
  if form.validate_on_submit():
    current_user.email = form.email.data
    if len(form.password.data)>5 and form.password.data == form.password2.data:
      current_user.set_password(form.password.data)

    db.session.commit()
    flash('Your profile has been updated.')
    return redirect(url_for('main.index'))
  return render_template('user/edit_profile.html', form=form)

@user.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
  p = Post.query.get_or_404(id)
  return render_template('post.html', post=p)

def allowed_file(filename):
  """ Helper function to determine what files are allowed """
  return ('.' in filename and \
    filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS'])

