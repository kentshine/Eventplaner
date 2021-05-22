import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# config
app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey764"

## Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#####################
#### Login ##########
#####################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from event_portal_main.users.views import users
from event_portal_main.core.views import core
from event_portal_main.event.views import events
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(events)