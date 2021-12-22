from ecoevent import app, db, login_manager
from flask import render_template, url_for, flash, redirect, request
from ecoevent.forms import RegisterForm, LoginForm, EventForm
from ecoevent.models import Users, Events, Attendance
import datetime
from flask_login import login_user, logout_user, login_required, current_user

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/")
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/register',methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(username=form.username.data,
                     email=form.email.data,
                     password=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Account successfully created. Welcome {user.username}", category="success")
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error while creating account: {err_msg}', category="danger")

    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and user.check_password(user_password=form.password.data):
            login_user(user)
            flash(f'Success! You are logged in as: {user.username}',category='success')
            return redirect(url_for('home_page'))
        else:
            flash("Username password don't match. Please try again",category='danger')

    return render_template("login.html",form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'Successfully logged out',category="info")
    return redirect(url_for('login_page'))

@app.route('/events',methods=['GET','POST'])
@login_required
def events_page():
    event_form = EventForm()
    if event_form.validate_on_submit():
        event = Events(event_name=event_form.name.data,
                       location=event_form.location.data,
                       event_time=datetime.datetime.strptime(event_form.time.raw_data[0],"%H:%M").time(),
                       event_date=datetime.datetime.strptime(str(event_form.date.raw_data[0]),"%Y-%m-%d").date(),
                       event_description=event_form.description.data,
                       creater=current_user.id)
        # event.create(current_user)
        db.session.add(event)
        db.session.commit()
        attend = Attendance(users_id=current_user.id,event_id=event.id)
        db.session.add(attend)
        db.session.commit()
        flash(f"Event successfully created.", category="success")
        return redirect(url_for("events_page"))
    if event_form.errors != {}:
        print(datetime.datetime.strptime(str(event_form.date.raw_data[0]),"%Y-%m-%d").date())
        for cause,err_msg in event_form.errors.items():
            flash(f'There was an error while creating Event:{cause} : {err_msg}', category="danger")

    events = Events.query.all()
    att = Attendance.query.filter_by(users_id=current_user.id).all()
    myEvents = set()
    for i in att:
        event = Events.query.filter_by(id=i.event_id).first()
        if event:
            myEvents.add(event)
    myEvents = list(myEvents)
    events.sort(key=lambda x:x.event_date)
    myEvents.sort(key=lambda x: x.event_date)
    return render_template("events.html", events=events, event_form=event_form, myEvents=myEvents)


@app.route("/attend_event",methods=['POST'])
def attend_event():
    event_id = request.form.get('event')
    event = Events.query.filter_by(id=event_id).first()
    event.attend(current_user)
    return redirect(url_for("events_page"))

@app.route('/cancel_event',methods=['POST'])
def cancel_event():
    event_id = request.form.get('cancelE')
    event = Events.query.filter_by(id=event_id).first()
    event.cancel(current_user)
    return redirect(url_for("events_page"))