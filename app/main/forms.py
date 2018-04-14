# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField, \
    FloatField, RadioField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Member, Home


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
            raise ValidationError("操作有误！")


class AddHomeForm(FlaskForm):
    """添加Home记录表单"""
    account = StringField(
        label="识别号",
        validators=[
            DataRequired("请输入识别号")
        ],
        description="identity name",
        render_kw={
            "class": "form-control",
            "placeholder": "Identity Name"
        }
    )
    nickname = StringField(
        label="Nickname",
        validators=[
            DataRequired("Please enter a nickname")
        ],
        description="nickname",
        render_kw={
            "class": "form-control",
            "placeholder": "Nick Name"
        }
    )
    net_asset = FloatField(
        label="Net Asset",
        validators=[
            DataRequired("Please enter a valid number")
        ],
        description="Net Asset",
        render_kw={
            "class": "form-control",
            "placeholder": "Net Asset"
        }
    )
    asset = FloatField(
        label="Asset",
        validators=[
            DataRequired("Please enter valid number")
        ],
        description="Asset",
        render_kw={
            "class": "form-control",
            "placeholder": "Asset"
        }
    )
    debt = FloatField(
        label="Debt",
        validators=[
            DataRequired("Please enter a valid number")
        ],
        description="Debt",
        render_kw={
            "class": "form-control",
            "placeholder": "Net Asset"
        }
    )
    cash = FloatField(
        label="Cash",
        validators=[
            DataRequired("Please enter a valid number")
        ],
        description="Cash",
        render_kw={
            "class": "form-control",
            "placeholder": "Cash"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_account(self, field):
        account = field.data
        home = Home.query.filter_by(account=account).count()
        if home > 0:
            raise ValidationError("Home名已存在")


class IssueDailyLogForm(FlaskForm):
    """申报项目表单"""
    category = RadioField(
        label='集体项目',
        validators=[
            DataRequired("Please pick one!")
        ],
        coerce=str,
        choices=[],
        render_kw={
            "type": "radio",
            "name ": "options",
            "autocomplete": "off",
        }
    )
    amount = FloatField(
        label="数额",
        validators=[
            DataRequired("必须输入一个数额")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入数额"
        }
    )
    content = TextAreaField(
        label="备注",
        render_kw={
            "class": "form-control",
            "placeholder": "请写下简单描述, 如:买菜, 电费, 车险"
        }
    )
    submit = SubmitField(
        "提交",
        render_kw={
            "class": "btn btn-primary btn-block"
        }
    )

    def validate_type(self, field):
        type = field.data
        if type == None:
            raise ValidationError("必须选择其中一项")

