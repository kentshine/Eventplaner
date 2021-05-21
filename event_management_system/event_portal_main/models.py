from event_portal_main import db,login_manager
from datetime  import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key = True)
    profile_image = db.Column(db.String(20),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship("Event",backref="organiser",lazy=True)


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username : {self.username}"


class Event(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.String, nullable=False)
    title = db.Column(db.String(140),nullable=False)
    description = db.Column(db.Text,nullable=False)
    participants = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String,nullable=False)

    def __init__(self,date,title,description,user_id,particpants,location):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.date = date
        self.participants = particpants
        self.location = location

    def __repr__(self):
        return f"Event id {self.id} --- Date : {self.date} --- Title : {self.title}"

