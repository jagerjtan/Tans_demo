# coding: utf8
from functools import wraps
from . import admin
from app import db, app
from flask import render_template, url_for, redirect, flash, request, session
from app.admin.forms import LoginForm, PwdForm, RegisterForm
from app.models import Admin, Adminlog


# 访问限制装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" in session and "admin_id" in session:
            flash("online", "ok")
            return f(*args, **kwargs)
        else:
            flash("offline", "err")
            return redirect(url_for("admin.login", next=request.url))

    return decorated_function


@admin.route("/", methods=['GET'])
@admin_login_req
def index():
    return render_template("admin/index.html")


@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "admin" in session and "admin_id" in session:
        flash("你已登录，请不要重复登录", "err")
        return redirect(request.args.get("next") or url_for("admin.index"))
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(account=data["account"]).first()
        if not admin.check_pwd(data['pwd']):
            flash("账户和密码不匹配", "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        adminlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        #
        # 待添加登录时间添加到日志数据库的操作
        #
        flash("登录成功！", "ok")
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout", methods=['GET'])
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for('admin.login'))


@admin.route("/pwd/", methods=['GET', 'POST'])
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


@admin.route("/account/", methods=['GET', 'POST'])
@admin_login_req
def account():
    form1 = PwdForm()
    return render_template("admin/account.html", form1=form1)


@admin.route("/register", methods=['GET', 'POST'])
@admin_login_req
def register():
    form = RegisterForm()
    return render_template("admin/register.html", form=form)
