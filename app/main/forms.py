# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Member


class LoginForm(FlaskForm):
    """成员登录表单"""
    account = StringField(
        label="帐号",
        validators=[
            DataRequired("请输入帐号！")
        ],
        description="帐号",
        render_kw={
            "class": "form-control",
            "placeholder": "帐号",
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
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        member = Member.query.filter_by(account=account).count()
        if member == 0:
            raise ValidationError("帐号和密码不匹配！")


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="原密码",
        validators=[
            DataRequired("请输入原密码")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入原密码"
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
            DataRequired("请确认新密码"),
            EqualTo("new_pwd", "两次密码输入不一致！")
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
        name = session['member']
        member = Member.query.filter_by(
            account=name
        ).first()
        if not member.check_pwd(pwd):
            print('haha')
            raise ValidationError("操作有误！")
