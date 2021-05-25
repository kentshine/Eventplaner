from event_portal_main import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


registered = db.Table('registered',
                db.Column('user_id',db.Integer,db.ForeignKey('users.id'),primary_key=True),
                db.Column('event_id',db.Integer,db.ForeignKey('events.id'),primary_key=True)
            )


class User(db.Model,UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key = True)
    profile_image = db.Column(db.String(20),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship("Event",backref="organiser",lazy=True)
    registered_events = db.relationship('Event', secondary=registered, backref=db.backref('coming', lazy='dynamic'))

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username : {self.username}"


class Event(db.Model):
    __tablename__ = 'events'
    users = db.relationship(User)
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.String, nullable=False)
    title = db.Column(db.String(140),nullable=False)
    description = db.Column(db.Text,nullable=False)
    participants = db.Column(db.Integer,nullable=False)
    location = db.Column(db.String,nullable=False)
    banner = db.Column(db.String,nullable=False)

    def __init__(self,date,title,description,user_id,participants,location,banner):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.date = date
        self.participants = participants
        self.location = location
        self.banner = banner

    def __repr__(self):
        return f"Event id {self.id} --- Date : {self.date} --- Title : {self.title}"

