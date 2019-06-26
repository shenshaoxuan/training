from app.extensions import login_manager
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.extensions import db
from app.model.vote import Vote

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(24), unique=True, nullable=False)
    _password = Column('password', String(100))
    vote = db.relationship('Vote', backref='user', lazy='dynamic')
    course = db.relationship('Course', backref='user', lazy='dynamic')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def is_vote(self, course_id):
        vote = self.vote.filter(Vote.course_id==course_id, Vote.user_id==self.id).first()
        if vote:
            return True
        return False

@login_manager.user_loader
def loader_user(uid):
    return User.query.get(uid)
