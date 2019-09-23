from flask import render_template,request,redirect,url_for,abort
from . import main
# from ..request import get_movies,get_movie,search_movie
from .forms import PitchForm,UpdateProfile, CommentForm
# from .forms import UpdateProfile
from .. import db,photos
from ..models import User, Pitch,Category,Comment,Upvote,Downvote
from flask_login import login_required,current_user
import markdown2 
from sqlalchemy import func
from sqlalchemy.orm import session

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    
    interviewpitches = Pitch.query.filter_by(category="Interview-Pitch").order_by(Pitch.posted.desc()).all()
    productpitches = Pitch.query.filter_by(category="Product-Pitch").order_by(Pitch.posted.desc()).all()
    promotionpitches = Pitch.query.filter_by(category="Promotion-Pitch").order_by(Pitch.posted.desc()).all()
    businesspitches = Pitch.query.filter_by(category="Business-Pitch").order_by(Pitch.posted.desc()).all()

    pitches = Pitch.query.filter_by().first()
    upvotes = Upvote.get_all_upvotes(pitch_id=Pitch.id)
    downvotes = Downvote.get_all_downvotes(pitch_id=Pitch.id)
    

    title = 'Welcome to the Pitches  website'

    return render_template('index.html', title = title)

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




# #  
# @main.route('/category/pitch/new/<int:id>', methods = ['GET','POST'])
# @login_required
# def new_picth(id):
#     form = PitchForm()
#     category = get_category(id)

#     if form.validate_on_submit():
#         cat_name = form.cat_name.data
#         pitch = form.pitch.data
        
#            # Updated review instance
#         new_pitch = Pitch(category_id=category.id,category_cat_name=cat_name,category_pitch=pitch,user=current_user)
#         # new_review = Review(movie.id,title,movie.poster,review)
#         # new_review.save_review()
#         # return redirect(url_for('movie',id = movie.id ))

#         # save review method
#         new_picth.save_pitch()
#         return redirect(url_for('.category',id = category.id ))

#     title = f'{category.title} pitch'
#     return render_template('new_pitch.html',title = title, pitch_form=form, category=category)

# @main.route('/pitch/<int:id>')
# def single_pitch(id):
#     pitch=Pitch.query.get(id)
#     if pitch is None:
#         abort(404)
#     format_pitch = markdown2.markdown(pitch.category_pitch,extras=["code-friendly", "fenced-code-blocks"])
#     return render_template('pitch.html',pitch = pitch,format_pitch=format_pitch)


@main.route('/user/<uname>')
def profile(uname):
    '''
    View profile page function that returns the profile page and its data
    '''
    user = User.query.filter_by(username = uname).first()
    title = f"{uname.capitalize()}'s Profile"

    get_pitches = Pitch.query.filter_by(author = User.id).all()
    get_comments = Comment.query.filter_by(user_id = User.id).all()
    get_upvotes = Upvote.query.filter_by(user_id = User.id).all()
    get_downvotes = Downvote.query.filter_by(user_id = User.id).all()

    if user is None:
        abort (404)

    return render_template("profile/profile.html", user = user, title=title, pitches_no = get_pitches, comments_no = get_comments, upvotes_no = get_upvotes, downvotes_no = get_downvotes)





@main.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    '''
    View home function that returns the home page
    '''
    interviewpitches = Pitch.query.filter_by(category="Interview-Pitch").order_by(Pitch.posted.desc()).all()
    productpitches = Pitch.query.filter_by(category="Product-Pitch").order_by(Pitch.posted.desc()).all()
    promotionpitches = Pitch.query.filter_by(category="Promotion-Pitch").order_by(Pitch.posted.desc()).all()
    businesspitches = Pitch.query.filter_by(category="Business-Pitch").order_by(Pitch.posted.desc()).all()
    # all_pitches = Pitch.get_all_pitches()
    pitch = Pitch.get_all_pitches()
    # print(all_pitches)

    title = 'Home | One Min Pitch'
    return render_template('home.html', title = title, pitch = pitch, interviewpitches = interviewpitches, productpitches = productpitches, promotionpitches = promotionpitches, businesspitches = businesspitches)


@main.route('/pitch/new',methods = ['GET','POST'])
@login_required
def pitch():
    '''
    View pitch function that returns the pitch page and data
    '''
    pitch_form = PitchForm()
    my_likes = Like.query.filter_by(pitch_id=Pitch.id)

    if pitch_form.validate_on_submit():
        content = pitch_form.content.data
        category = pitch_form.category.data
        pitch_title = pitch_form.pitch_title.data

        new_pitch = Pitch(pitch_title=pitch_title, content=content, category = category, user = current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))


    title = 'New Pitch | One Minute Pitch'
    return render_template('pitch.html', title = title, pitch_form = pitch_form, upvotes = my_likes)


@main.route('/pitch/<int:pitch_id>/comment',methods = ['GET', 'POST'])
@login_required
def comment(pitch_id):
    '''
    View comments page function that returns the comment page and its data
    '''
    # comment_form = CommentForm()

    comment_form = CommentForm()
    my_pitch = Pitch.query.get(pitch_id)
    if my_pitch is None:
        abort(404)

    if comment_form.validate_on_submit():
        comment_content = comment_form.comment_content.data

        new_comment = Comment(comment_content=comment_content, pitch_id = pitch_id, user = current_user)
        new_comment.save_comment()

        return redirect(url_for('.comment', pitch_id=pitch_id))

    all_comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    # all_comments = Comment.get_all_comments(id)
    # all_comments = Comment.get_all_comments(pitch_id)
    title = 'New Comment | One Min Pitch'

    return render_template('comment.html', title = title, pitch=my_pitch ,comment_form = comment_form, comment = all_comments )





@main.route('/pitch/<int:pitch_id>/upvote',methods = ['GET','POST'])
@login_required
def upvote(pitch_id):
    '''
    View upvote function that returns likes
    '''
    my_pitch = Pitch.query.get(pitch_id)
    user = current_user

    pitch_upvotes = Upvote.query.filter_by(pitch_id=pitch_id)


    if Upvote.query.filter(Upvote.user_id==user.id,Upvote.pitch_id==pitch_id).first():
        return  redirect(url_for('.index'))

    new_upvote = Upvote(pitch_id=pitch_id, user = current_user)
    new_upvote.save_upvotes()
    return redirect(url_for('.index'))



@main.route('/pitch/<int:pitch_id>/downvote',methods = ['GET','POST'])
@login_required
def downvote(pitch_id):
    '''
    View downvote function that returns dislikes
    '''
    my_pitch = Pitch.query.get(pitch_id)
    user = current_user

    pitch_downvotes = Downvote.query.filter_by(pitch_id=pitch_id)

    if Downvote.query.filter(Downvote.user_id==user.id,Downvote.pitch_id==pitch_id).first():
        return redirect(url_for('.index'))

    new_downvote = Downvote(pitch_id=pitch_id, user = current_user)
    new_downvote.save_dislikes()
    return redirect(url_for('.index'))
