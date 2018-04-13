# coding: utf8
from functools import wraps
from . import main
from app import db
from flask import render_template, url_for, redirect, flash, request, session
from app.main.forms import LoginForm, PwdForm
from app.models import Member, Memberlog
from app.decorators import member_login_req




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
        flash("登录成功！", "ok")
        flash("online", "mem1")
        return redirect(request.args.get("next") or url_for("main.index"))
    return render_template("main/login.html", form=form)


@main.route("/logout", methods=['GET'])
def logout():
    if '_flashes' in session:
        msg = session['_flashes']
        session.clear()
        session['_flashes'] = msg
    else:
        session.clear()
    flash("You've logged out.", "ok")
    return redirect(url_for('main.login'))


@main.route("/pwd/", methods=['GET', 'POST'])
@member_login_req
def pwd():
    return render_template("main/pwd.html")


@main.route("/account/<int:id>", methods=['GET','POST'])
@member_login_req
def account(id=None):
    data = {}
    if id == 202:
        id = int(session['member_id'])
    try:
        member = Member.query.filter_by(account=session['member']).first()
        last_memberlogin = member.memberlogs[-1]
        data = {
            'name': member.account,
            'last_login': last_memberlogin.addtime,
            'ip': last_memberlogin.ip,
            'face': member.face
        }
    except BaseException as e:
        flash(e, "err")
    form1 = PwdForm()
    if form1.validate_on_submit():
        from werkzeug.security import generate_password_hash
        member.pwd = generate_password_hash(form1.data['new_pwd'])
        db.session.add(member)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for("main.logout"))
    #
    # 预留form2给其他修改表单，例如编辑信息，增删查改记录
    #

    return render_template("main/account.html", id=id, form1=form1, data=data)
