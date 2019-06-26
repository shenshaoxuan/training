from sqlalchemy import Column, Integer, ForeignKey

from app.extensions import db



class Vote(db.Model):
    __tablename__ = 'vote'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_id =Column(Integer, ForeignKey('users.id'), nullable=False)

