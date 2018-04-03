# coding: utf8
from . import admin
from flask import render_template, url_for, redirect, flash, request, session
from app.admin.forms import LoginForm
from app.models import Admin


@admin.route("/", methods=['GET'])
def index():
    return render_template("admin/index.html")


@admin.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "admin" in session and "admin_id" in session:
        flash("你已登录，请不要重复登录", "err")
        return redirect(url_for("admin.index"))
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(account=data["account"]).first()
        if not admin.check_pwd(data['pwd']):
            flash("账户和密码不匹配", "err")
            return  redirect(url_for("admin.login"))
        session["admin"] = data["account"]
        session["admin_id"] = admin.id
        #
        # 待添加登录时间添加到日志数据库的操作
        #
        flash("登录成功！","ok")
        return redirect(url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout", methods=['GET'])
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for('admin.adminlogin'))


@admin.route("/pwd/", methods=['GET', 'POST'])
def pwd():
    return render_template("admin/pwd.html")


@admin.route("/account/", methods=['GET'])
def account():
    return render_template("admin/account.html")
