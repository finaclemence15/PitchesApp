from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
# from .forms import PitchForm,UpdateProfile
from .forms import UpdateProfile
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

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


#  
@main.route('/category/pitch/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_picth(id):
    form = PitchForm()
    category = get_category(id)

    if form.validate_on_submit():
        cat_name = form.cat_name.data
        pitch = form.pitch.data
        
           # Updated review instance
        new_pitch = Pitch(category_id=category.id,category_cat_name=cat_name,category_pitch=pitch,user=current_user)
        # new_review = Review(movie.id,title,movie.poster,review)
        # new_review.save_review()
        # return redirect(url_for('movie',id = movie.id ))

        # save review method
        new_picth.save_pitch()
        return redirect(url_for('.category',id = category.id ))

    title = f'{category.title} pitch'
    return render_template('new_pitch.html',title = title, pitch_form=form, category=category)

@main.route('/pitch/<int:id>')
def single_pitch(id):
    pitch=Pitch.query.get(id)
    if pitch is None:
        abort(404)
    format_pitch = markdown2.markdown(pitch.category_pitch,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('pitch.html',pitch = pitch,format_pitch=format_pitch)