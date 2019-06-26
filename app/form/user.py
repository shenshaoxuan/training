from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from app.model.user import User


# 用户注册
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Length(2, 10, message='用户名必须在2~10个字符之间')], default='请输入真实姓名')
    password = PasswordField('密码', validators=[Length(4, 12, message='密码长度必须在4~12个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    submit = SubmitField('立即注册')

    # 自定义验证函数，验证username
    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('该用户已注册，请选用其他名称')
        return True


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')




