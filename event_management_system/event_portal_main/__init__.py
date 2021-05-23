import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail,Message

# config
app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey764"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USERNAME'] = "bostonpublicschooleventportal@gmail.com"
app.config['MAIL_PASSWORD'] = "BOSTON9846"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TSL'] = False
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False


## Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
mail = Mail(app)


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