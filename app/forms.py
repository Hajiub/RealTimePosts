from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms import validators

from .models import User


class LoginForm(FlaskForm):
    username = StringField(u'Username', validators=[validators.DataRequired()])
    password = PasswordField(u'Password', validators=[validators.optional()])

    def validate_on_submit(self):
        check_validate = super(LoginForm, self).validate_on_submit()

        # if our validators do not pass
        if not check_validate:
            return False

        # Does our the exist
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username')
            return False

        # Do the passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid password')
            return False

        return True
class SignInForm(FlaskForm):
    username = StringField(u'Username', validators=[validators.DataRequired()])
    password = PasswordField(u'Password', validators=[validators.optional()])
    confirm_pass = PasswordField(u'Confirm Password', validators=[validators.EqualTo('password', message="Password must match")])
    def validate_on_submit(self):
        check_validate = super(SignInForm, self).validate_on_submit()

        if not check_validate:
            return False

        # Make sure that the username is unique
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already exists')
            return False
        
        # Make sure that the password is more than or equal to 8 chars
        if len(self.password.data) < 7:
            self.password.errors.append('Password must be at least 8 chars.')
            return False
        return True
class CreatePostForm(FlaskForm):
    content = TextAreaField(u'Content', validators=[validators.DataRequired(), validators.Length(min=5, message="You post should contain more chars!")])
    create  = SubmitField(u'Create')
    