# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label="账户",
        validators=[
            DataRequired("请输入账户！")
        ],
        description="账户",
        render_kw={
            "class": "form-control",
            "placeholder": "账户",
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
            "placeholder": "密码",
        }
    )
    submit = SubmitField(
        "Login",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(account=account).count()
        if admin == 0:
            return None
            # raise ValidationError("帐号和密码不匹配！") 这里不给提示是因为防止有人不断利用不存在的账号来检测存在的账号

class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入旧密码"
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码"
        }
    )
    re_pwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请确认新密码")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "再次输入新密码"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session['admin']
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误")

