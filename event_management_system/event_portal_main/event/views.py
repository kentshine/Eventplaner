from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from flask_login import current_user,login_required
from event_portal_main import db
from event_portal_main.models import Event,User
from event_portal_main.event.picture_handler import add_event_banner
from event_portal_main import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import datetime


events = Blueprint('events',__name__)
s = URLSafeTimedSerializer("AMONGUS")
@events.route("/create",methods=["GET","POST"])
@login_required
def create_event():
    if request.method == "POST":
        title = request.form.get('name')
        date = request.form.get('date').replace("T" , " ")
        file = request.files['banner']
        participants = request.form.get('participants')
        location = request.form.get('location')
        description = request.form.get('description')
        banner = add_event_banner(file , title,1800,800)

        event = Event(user_id=current_user.id,title=title,date=date,participants=participants,location=location,description=description,banner=banner)
        print(event)
        db.session.add(event)
        db.session.commit()
        flash('Event sucessfully created')
        return redirect(url_for('core.home'))

    return render_template('create_event.html')


@events.route('/<int:event_id>',methods=["POST","GET"])
@login_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    id = current_user.id
    number_of_participants = event.coming.count()
    today = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
    if request.method == "POST":

        user = User.query.filter_by(id=id).first()
        if user is not None:
            token = s.dumps(user.email,salt="rsvp-letter")
            msg = Message("RSVP MODULE",sender='bostonpublicschooleventportal@gmail.com',recipients=[user.email])
            link = url_for("events.confirmed_rsvp" , token=token,event_id=event.id,_external=True)
            msg.body = "BostonEdPortal has sent you an rsvp invitation"
            msg.html = render_template("rsvp.html",link=link,event=event)
            mail.send(msg)
            return redirect(url_for("events.view_event",event_id=event.id))
        else:
            flash("Please give username same as your account username")
            request.form["name"] = ""

    elif request.method == "GET":
        return render_template("view_event.html",event=event,number_of_participants=number_of_participants,today=today)

@events.route("/rsvp/<token>/<int:event_id>/")
def confirmed_rsvp(token,event_id):
    email = s.loads(token,salt="rsvp-letter",max_age=100)
    print(email)
    user = User.query.filter_by(email=email).first()
    event = Event.query.filter_by(id = event_id).first()
    registered_before = False
    for students in event.coming:
        if students.username == user.username:
            registered_before = True


    if registered_before == False:
        event.coming.append(user)
        db.session.commit()
        return render_template("thankyou.html")
    else:
        return render_template("Already_Registered.html")



@events.route('/rejected_rsvp')
def rejected_rsvp():
    return render_template("rejected.html")

@events.route("/<int:event_id>/delete",methods=["POST","GET"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.organiser != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash("Event is deleted !")
    return redirect(url_for('core.home'))
