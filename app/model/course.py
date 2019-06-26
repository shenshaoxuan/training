from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from app.extensions import db



class Course(db.Model):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    category = Column(Integer, doc='语言技巧=1, 框架=2, 数据库=3, 新技术=4', nullable=False)
    teach_or_listen = Column(Integer, doc='讲课=1, 听课=2')
    course_name = Column(String(24), unique=True, nullable=False)
    remark = Column(String(500), nullable=False)
    create_time = Column(DateTime, default=datetime.now, nullable=False)
    user_id =Column(Integer, ForeignKey('users.id'), nullable=False)

