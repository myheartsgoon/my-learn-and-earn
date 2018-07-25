from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired('请输入用户名！')])
    password = PasswordField('密码', validators=[DataRequired('请输入密码！')])
    login = SubmitField('登陆')


class PublishForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题！'), Length(max=50, message='标题最长为50位')],
                        render_kw={"placeholder": "标题"})
    descp = TextAreaField('简介', validators=[DataRequired('请输入简介！'), Length(max=150, message='简介最长为150位')],
                          render_kw={"placeholder": "简介"})
    content = TextAreaField('正文', validators=[DataRequired('请输入正文！'), Length(max=10000, message='正文最长为10000位')],
                            render_kw={"placeholder": "正文"})
    publish = SubmitField('发表')
