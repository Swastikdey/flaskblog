from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
            


class PostForm(FlaskForm):
    title=StringField('Title',validators=[DataRequired(message="Title is required.")])
    content=TextAreaField('Content',validators=[DataRequired(message="Content is required."),Length(min=10)])
    submit=SubmitField('Post')

