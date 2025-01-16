from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from my_app.models import User
from flask_login import current_user
            

class RegistrationForm(FlaskForm):
    username=StringField('Username', 
                         validators=[DataRequired(),Length(min=2, max=20)])
    email=StringField('Email',
                      validators=[DataRequired(),Email()])
    password=PasswordField('Password',
                           validators=[DataRequired(), ])
    confirm_password=PasswordField('Confirm Password',
                           validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists. Please choose another username")

    def validate_email(self,email):
            email=User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists. Please choose another email")



class LoginForm(FlaskForm):
    email=StringField('Email',
                      validators=[DataRequired(),Email()])
    password=PasswordField('Password',
                           validators=[DataRequired(), ])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Log In') 

class UpdateForm(FlaskForm):
    username=StringField('Username', 
                         validators=[DataRequired(),Length(min=2, max=20)])
    email=StringField('Email',
                      validators=[DataRequired(),Email()])
    picture=FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists. Please choose another username")

    def validate_email(self,email):
        if email.data!=current_user.email:
            email=User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email already exists. Please choose another email")

class RequestResetPasswordForm(FlaskForm):
    email=StringField('Email',
                    validators=[DataRequired(),Email()])
    submit=SubmitField('Request password change')

    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError("Email doesnot exist.")
        
class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',
                           validators=[DataRequired() ])
    confirm_password=PasswordField('Confirm Password',
                           validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Reset Password')
    
    