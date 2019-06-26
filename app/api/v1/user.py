from flask import Blueprint, flash, redirect, request, url_for, render_template
from flask_login import login_user, logout_user

from app.extensions import db
from app.form.user import RegisterForm, LoginForm
from app.model.user import User

user = Blueprint('user', __name__, url_prefix='/v1/user/')

@user.route('/logout/')
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('main.index'))

@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif u.check_password(form.password.data):
            # 用户登录，顺便可以完成记住我的功能，还可以指定有效时间
            login_user(u, remember=form.remember.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('无效的密码')
    return render_template('user/login.html', form=form)

@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,
                 password=form.password.data)
        # 然后保存到数据库中
        db.session.add(u)
        # 此时还没有提交，所以新用户没有id值，需要手动提交
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)



