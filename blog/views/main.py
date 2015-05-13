from flask import Blueprint, render_template, redirect
from blog.extensions import cache

main = Blueprint('main', __name__)


@main.route('/')
def index():
  return render_template('index.html')

@main.route('/login')
def login():
  return 'Login'

@main.route('/logout')
def logout():
  return 'Logout'
