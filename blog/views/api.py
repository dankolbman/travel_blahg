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

@api.route('/<string:username>/<string:api_key>/pings', methods=['GET', 'POST'])
def pings(username, api_key):
  data = request.get_json()
  print(len(data['points']),'incoming points')
  new = 0
  dupes = 0
  user = User.query.filter_by(username=username).first_or_404()
  if user.api_key == api_key:
    for point in data['points']:
      ts = point['timestamp']/1000
      ts = datetime.utcfromtimestamp(ts)
      # Check if this point has already been reported
      if not Ping.query.filter_by(author=user).filter_by(timestamp=ts).first():
        ping = Ping(author=user, timestamp=ts,
            accuracy=point['accuracy'],
  	    loc='POINT({0} {1})'.format(point['longitude'],point['latitude']))
        db.session.add(ping)
        new += 1
      else:
        dupes += 1
    db.session.commit()
    print('New:',new,'Duplicate:',dupes)
    return "Processed new points"
  else:
    print('Bad AUTH')
    return "Bad AUTH"

@api.route('/<string:username>/<string:api_key>/ping', methods=['GET', 'POST'])
def ping(username, api_key):
  data = request.get_json()
  print(data)
  user = User.query.filter_by(username=username).first_or_404()
  if user.api_key == api_key:
    ts = data['timestamp']/1000
    ts = datetime.utcfromtimestamp(ts)
    # Check if this point has already been reported
    if not Ping.query.filter_by(author=user).filter_by(timestamp=ts).first():
      ping = Ping(author=user, timestamp=ts,accuracy=data['accuracy'],
  	    loc='POINT({0} {1})'.format(data['longitude'],data['latitude']))
      db.session.add(ping)
      db.session.commit()
      return "New point"
    else:
      print("Duplicate ping")
      return "Duplicate point"
  else:
    print('Bad AUTH')
    return "Bad AUTH"

@api.route('/<string:username>/<string:api_key>', methods=['GET', 'POST'])
def test(username, api_key):
  user = User.query.filter_by(username=username).first_or_404()
  if user.api_key == api_key:
    return "Good AUTH"
  else:
    return "Bad AUTH"

