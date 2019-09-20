from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
# from .forms import ReviewForm,UpdateProfile
from .. import db,photos
from ..models import User
from flask_login import login_required,current_user
import markdown2 

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    title = 'Welcome to the Piches  website'

    return render_template('index.html', title = title)
