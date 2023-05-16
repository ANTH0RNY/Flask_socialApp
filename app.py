import os
from app import db, create_app
from flask_migrate import Migrate

conf = os.environ.get('APP_CONFIG') or 'default'
# print(conf)
app = create_app(conf)

migrate =  Migrate(app, db)
