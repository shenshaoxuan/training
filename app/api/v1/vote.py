from flask import Blueprint, render_template
from flask_login import  current_user
from sqlalchemy import func
from flask_login import login_required

from app.extensions import db
from app.model.course import Course
from app.model.user import User
from app.model.vote import Vote

vote = Blueprint('vote', __name__, url_prefix='/v1/vote/')

# 查询出所有提交的课程
@vote.route('/get/<int:teach_or_listen>/')
@login_required
def get_all_course(teach_or_listen):
    courses = Course.query.filter(Course.teach_or_listen==teach_or_listen).order_by(Course.category).all()
    print(teach_or_listen)
    return render_template('vote/show.html', courses=courses, teach_or_listen=teach_or_listen)


# 投票和取消投票，ajax请求
@vote.route('/course/<int:course_id>')
@login_required
def vote_course(course_id):
    if  not current_user.is_vote(course_id):
        vote = Vote(course_id=course_id, user_id=current_user.id)
        db.session.add(vote)
    else:
        vote = current_user.vote.filter(Vote.course_id==course_id).first()
        db.session.delete(vote)
    db.session.commit()
    return '123'

def query():
    courses = db.session.query(Course, func.count(Vote.id).label('quantity'),
                               func.group_concat(Vote.user_id).label('c')). \
        select_from(Course). \
        join(Vote, Vote.course_id == Course.id, isouter=True). \
        group_by(Course.id).order_by(func.count(Vote.id).label('quantity').desc()).all()
    results = []
    for course in courses:
        quantity = course.quantity
        id = course.Course.id
        if course.Course.teach_or_listen == 1:
            teacher = course.Course.user.username
        else:
            teacher = '-'
        category = course.Course.category
        course_name = course.Course.course_name
        remark = course.Course.remark
        create_time = course.Course.create_time
        student = course.c
        if student is None:
            student = '-'
        else:
            users = User.query.filter(User.id.in_(student.split(','))).all()
            student = ','.join(user.username for user in users)
        d = {'quantity': quantity, 'id': id, 'teacher': teacher, 'category': category, 'course_name': course_name,
             'remark': remark, 'create_time': create_time, 'student': student}
        results.append(d)
    return results

@vote.route('/hot/')
@login_required
def hot_course():
    results = query()
    return render_template('vote/hot.html', results=results)

@vote.route('/get_one/<int:id>/')
@login_required
def get_one(id):
    results = query()
    return render_template('vote/detail.html', result=list(filter(lambda x:x['id']==id, results))[0])





