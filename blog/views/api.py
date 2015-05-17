from datetime import datetime

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, jsonify
from flask.ext.login import login_required, current_user

from blog.extensions import cache
from blog.models import db
from blog.models import User, Post, TextPost, ImagePost, Ping

api = Blueprint('api', __name__)

@api.route('/')
def api_home():
  return 'hi'

@api.route('/<string:username>/<string:api_key>/ping', methods=['GET', 'POST'])
def ping(username, api_key):
  print(request.json)
  return str(request.json)

@api.route('/<string:username>/<string:api_key>/ping/<float:lat>/<float:log>', methods=['GET', 'POST'])
def ping_loc(username, api_key, lat, log):
  user = User.query.filter_by(username=username).first_or_404()
  if user.api_key == api_key:
    p = Ping(author=user, timestamp=datetime.utcnow(), latitude=lat, longitude=log)
    db.session.add(p)
    db.session.commit()
    return 'success'
  else:
    return 'invalid key'

