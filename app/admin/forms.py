# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="帐号",
        validators=[
            DataRequired("请输入帐号！")
        ],
        description="帐号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入帐号！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！"),
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(account=account).count()
        if admin == 0:
            raise ValidationError("帐号和密码不匹配！")
