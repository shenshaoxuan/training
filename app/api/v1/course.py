from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.form.course import CourseForm
from app.model.course import Course
from app.model.user import User
from app.model.vote import Vote

course = Blueprint('course', __name__, url_prefix='/v1/course/')

@course.route('/get/<int:teach_or_listen>/')
@login_required
def get_course(teach_or_listen):
    courses = Course.query.filter(Course.user_id==current_user.id,
                                  Course.teach_or_listen==teach_or_listen).\
        order_by(Course.category, Course.create_time)\
        .all()
    return render_template('course/show.html', courses=courses)


@course.route('/add/', methods=['GET', 'POST'])
@login_required
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course.query.filter(Course.course_name == form.course_name.data).first()
        if course:
            flash('课程已被别人添加啦，请换一个吧!')
        else:
            course = Course(category=form.category.data,
                            teach_or_listen=form.teach_or_listen.data,
                            course_name=form.course_name.data,
                            remark=form.remark.data,
                            user_id=current_user.id)

            # 然后保存到数据库中
            db.session.add(course)
            # 此时还没有提交，所以新用户没有id值，需要手动提交
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('course.get_course', teach_or_listen=form.teach_or_listen.data))
    return render_template('course/add.html', form=form)


@course.route('/get_one/<int:id>/', methods=['GET'])
@login_required
def get_one(id):
    form = CourseForm()
    course = Course.query.filter(Course.user_id==current_user.id, Course.id==id).first()
    return render_template('course/detail.html', form=form, course=course)


@course.route('/update/<int:id>/', methods=['GET', 'POST'])
@login_required
def update(id):
    course = Course.query.filter(Course.id == id).first()
    if not course:
        flash('找不到课程')
    form = CourseForm()
    if form.validate_on_submit():
        course.category=form.category.data
        course.teach_or_listen=form.teach_or_listen.data
        course.course_name=form.course_name.data
        course.remark=form.remark.data
        db.session.add(course)
        db.session.commit()
        flash('更新成功')
        return redirect(url_for('course.get_course', teach_or_listen=1))
    return render_template('course/update.html', course=course, form=form)


@course.route('/delete/<int:id>/', methods=['GET', 'POST'])
@login_required
def delete(id):
    votes = Vote.query.join(User, User.id==Vote.user_id).filter(Vote.course_id==id).all()
    course = Course.query.filter(Course.id == id).first()
    teach_or_listen = course.teach_or_listen

    if votes:
        flash('【% 等同学特别想听这门课,不能删除' % '、'.join(vote.user.username for vote in votes))
    else:
        db.session.delete(course)
        db.session.commit()
    return redirect(url_for('course.get_course', teach_or_listen=teach_or_listen))