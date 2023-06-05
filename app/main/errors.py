from flask import render_template, flash
from . import main

@main.app_errorhandler(404)
def error_404(e):
    flash('Page Not Found 😕')
    return render_template('main/index.html'), 404

@main.app_errorhandler(500)
def error_500(e):
    flash('Something went wrong 🙇')
    return render_template('main/index.html'), 500

@main.app_errorhandler(403)
def error_403(e):
    flash('You are not allowed to do that 🚫')
    return render_template('main/index.html'), 403