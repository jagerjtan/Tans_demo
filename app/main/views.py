# coding: utf8
from functools import wraps
from . import main
from app import db
from flask import render_template, url_for, redirect, flash, request, session
from app.main.forms import LoginForm
from app.models import Member, Memberlog

# 访问限制装饰器
def member_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "member" in session and "member_id" in session:
            flash("online", "ok")
            return f(*args, **kwargs)
        else:
            flash("offline", "err")
            return redirect(url_for("main.login", next=request.url))

    return decorated_function

@main.route("/", methods=['GET'])
@member_login_req
def index():
    return render_template("main/index.html")


@main.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "member" in session and "member_id" in session:
        flash("你已登录，请不要重复登录", "err")
        return redirect(request.args.get("next") or url_for("main.index"))
    if form.validate_on_submit():
        data = form.data
        member = Member.query.filter_by(account=data["account"]).first()
        if not member.check_pwd(data['pwd']):
            flash("账户和密码不匹配", "err")
            return redirect(url_for("main.login"))
        session["member"] = data["account"]
        session["member_id"] = member.id
        memberlog = Memberlog(
            member_id=member.id,
            ip=request.remote_addr
        )
        db.session.add(memberlog)
        db.session.commit()
        #
        # 待添加登录时间添加到日志数据库的操作
        #
        flash("登录成功！", "ok")
        return redirect(request.args.get("next") or url_for("main.index"))
    return render_template("main/login.html", form=form)


@main.route("/logout", methods=['GET'])
def logout():
    session.pop("member", None)
    session.pop("member_id", None)
    return redirect(url_for('main.login'))


@main.route("/pwd/", methods=['GET', 'POST'])
@member_login_req
def pwd():
    return render_template("main/pwd.html")


@main.route("/account/", methods=['GET'])
@member_login_req
def account():
    return render_template("main/account.html")
