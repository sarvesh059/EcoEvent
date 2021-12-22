from ecoevent import db, bcrypt
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username = db.Column(db.String(length=30),nullable=False, unique=True)
    email = db.Column(db.String(length=50),nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60),nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_password):
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def check_password(self,user_password):
        return bcrypt.check_password_hash(self.password_hash,user_password)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Events(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    event_name = db.Column(db.String(length=50), nullable=False)
    location = db.Column(db.String(length=256),nullable=False)
    event_date = db.Column(db.Date())
    event_time = db.Column(db.Time(), nullable=False)
    event_description = db.Column(db.String(length=1024), nullable=False, unique=True)
    creater = db.Column(db.Integer())

    def create(self,user):
        self.creater = user.id
        db.session.commit()

    def attend(self,user):
        attend = Attendance(users_id=user.id,event_id=self.id)
        db.session.add(attend)
        db.session.commit()

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def cancel(self,user):
        Attendance.query.filter_by(users_id=user.id).filter_by(event_id=self.id).delete()
        db.session.commit()

class Attendance(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    users_id = db.Column(db.Integer(),nullable=False)
    event_id = db.Column(db.Integer(),nullable=False)
