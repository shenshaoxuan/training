from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField


class CourseForm(FlaskForm):
    category = SelectField('课程类型', coerce=int, choices=[(1, '语言技巧'),(2, '框架'), (3, '数据库'), (4, '新技术')])
    teach_or_listen = SelectField('讲课或听课', coerce=int, choices=[(1, '我要讲课'),(2, '我要听课')])
    course_name = StringField('课程名字')
    remark = TextAreaField('详细')
    submit = SubmitField('保存')








