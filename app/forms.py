import wtforms
from flask.ext.login import current_user

from app import flask_bcrypt
from models import User


class SignUpForm(wtforms.Form):
    email = wtforms.StringField('Email', [wtforms.validators.InputRequired()])
    password = wtforms.StringField('Password', [wtforms.validators.InputRequired()])
    accept_rules = wtforms.BooleanField('I accept terms and conditions', [wtforms.validators.InputRequired()])

    def validate_email(form, field):
        user = User.objects(email=field.data).first()
        if user is not None:
            raise wtforms.ValidationError('This email is already taken')


class SignInForm(wtforms.Form):
    email = wtforms.StringField('Email', [wtforms.validators.InputRequired()])
    password = wtforms.StringField('Password', [wtforms.validators.InputRequired()])

    def validate_password(form, field):
        user = User.objects(email=form.email.data).first()
        if user is None:
            raise wtforms.ValidationError('Wrong email or password')
        if not user.check_password(field.data):
            raise wtforms.ValidationError('Wrong email or password')


class ProfileForm(wtforms.Form):
    current_password = wtforms.StringField('Current Password', [wtforms.validators.InputRequired()])
    new_password = wtforms.StringField('New Password', [wtforms.validators.InputRequired()])

    def validate_current_password(self, field):
        if not current_user.check_password(field.data):
            raise wtforms.ValidationError('Wrong password')