from flask import render_template,request,Blueprint,redirect,url_for
from event_portal_main import login_manager
from flask_login import login_required,current_user
from event_portal_main.models import Event,User
import datetime
core = Blueprint('core',__name__)


@core.route("/",methods=["GET","POST"])
def index():

    if request.form.get("login") == "Login":
        return redirect(url_for('users.login'))
    elif request.form.get("register") == "Register":
        return redirect(url_for('users.register'))

    return render_template("index.html")

@core.route("/home",methods=["GET","POST"])
@login_required
def home():
    page = request.args.get('page',1,type=int)
    events = Event.query.order_by(Event.date.asc()).paginate(page=page, per_page=4)
    user = User.query.filter_by(id=current_user.id).first()
    today = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
    return render_template("home.html",events=events,user=user,today=today)
