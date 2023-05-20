from flask import render_template, flash, request, url_for, redirect
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import login_Form
from ..models import User

@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = login_Form()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if not user:
            flash('Invalid email')
            return render_template('auth/login.html', form=form)
        if not user.verify_password(form.password.data):
            flash('Invalid email or password')
            return render_template('auth/login.html', form=form)
        login_user(user, form.remember_me.data)
        next = request.args.get('next')

        if next or next.startswith('/'):
            return redirect(next)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out have a nice day')
    return redirect(url_for('main.index'))