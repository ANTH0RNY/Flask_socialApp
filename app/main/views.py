from flask import render_template
from . import main
from .. import db


@main.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World'