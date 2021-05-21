from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import current_user,login_required
from event_portal_main import db
from event_portal_main.models import Event


events = Blueprint('events',__name__)

@events.route("/create",methods=["GET","POST"])
@login_required
def create_event():
    if request.method == "POST":
        title = request.form.get('name')
        date = request.form.get('date')
        particpants = request.form.get('participants')
        location = request.form.get('location')
        description = request.form.get('description')

        event = Event(user_id=current_user.id,title=title,date=date,particpants=particpants,location=location,description=description)
        print(event)
        db.session.add(event)
        db.session.commit()
        flash('Event sucessfully created')
        return redirect(url_for('core.home'))

    return render_template('create_event.html')



