

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Write something about yourself',validators=[Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    pitch_title = StringField('Title', validators=[Required()])
    content = TextAreaField('Your Pitch', validators=[Required()])
    category = SelectField('Category', choices=[('Interview-Pitch','Interview Pitch'),('Product-Pitch','Product Pitch'),('Promotion-Pitch','Promotion Pitch'),('Business-Pitch','Business Pitch')], validators=[Required()])
    submit = SubmitField('Pitch It!')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Leave your comments', validators=[Required()])
    submit = SubmitField('Comment')