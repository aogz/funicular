from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound

from app import login_manager
from forms import SignUpForm, SignInForm, ProfileForm
from models import User

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET'])
def index():
    return render_template('/auth/index.html')


@auth.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.form)
        if form.validate():
            current_user.set_password(form.new_password.data)
            current_user.save()
            flash({'type':'success', 'text':'Password updated'})
            return redirect('/')
    return render_template("/auth/profile.html", **locals())


@auth.route('/sign-in/', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.form)
        if form.validate():
            user = User.objects().get(email=form.email.data)
            if login_user(user, remember='yes'):
                current_app.logger.info('Signed In')
                flash({'type':'success', 'text':'Signed In'})
                return redirect('/')
            else:
                current_app.logger.info('login failed')
                flash({'type':'error', 'text':'Failed'})
    return render_template("/auth/sign-in.html", **locals())


@auth.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.form)
        if form.validate():
            user = User()
            user.email = form.email.data
            user.set_password(form.password.data)
            user.save()
            if login_user(user, remember="no"):
                flash({'type': 'info', 'text': 'Logged In!'})
            else:
                flash({'type': 'danger', 'text': 'failed to sign in'})
            return redirect('/')
    return render_template("/auth/sign-up.html", **locals())


@auth.route("/sign-out/")
@login_required
def sign_out():
    logout_user()
    flash({'type': 'info', 'text': 'Logged Out!'})
    return redirect('/')


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/')
    try:
        return User.objects().with_id(id)
    except User.DoesNotExist:
        return None

