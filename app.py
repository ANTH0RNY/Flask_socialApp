import os
from flask_migrate import Migrate
from app import db, create_app
from app.models import User, Role

conf = os.environ.get('APP_CONFIG') or 'default'
# print(conf)
app = create_app(conf)

@app.shell_context_processor
def shell_context():
    return dict(db=db, User=User, Role=Role)