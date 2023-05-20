from flask import render_template, flash, request, url_for, redirect
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import login_Form, register_Form
from ..models import User
from .. import db

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

        if next is None or not next.startswith('/'):
            return redirect(url_for('main.index'))
        return redirect(next)
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out have a nice day')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = register_Form()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        if User.query.filter_by(username=name).first() or User.query.filter_by(email=email).first():
            flash('Username or email is already taken')
            return render_template("auth/register.html", form=form)
        new_user = User(username=name, email=email)
        new_user.password = form.password.data
        db.session.add(new_user)
        db.session.commit()
        flash('Feel free to login')
        return redirect(url_for('auth.login'))
            
    return render_template("auth/register.html", form=form)