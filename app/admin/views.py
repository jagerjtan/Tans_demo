# coding: utf8
from functools import wraps
from . import admin
from app import db, app, socketio
from flask import render_template, url_for, redirect, flash, request, session
from app.admin.forms import LoginForm, PwdForm, RegisterForm
from app.models import Admin, Adminlog, Member
import shutil


# my graph
def test_graph():
    from pyecharts import Line, Style

    style = Style(
        width='100%'
    )

    attr,v1,v2,v3,v4 = [],[],[],[],[]
    line = Line("cpu们", **style.init_style)
    line.chart_id = 'cpus'
    line.add("cpu1", attr, v1, is_smooth="True", is_toolbox_show=False)
    line.add("cpu2", attr, v2, is_smooth="True")
    line.add("cpu3", attr, v3, is_smooth="True")
    line.add("cpu4", attr, v4, is_smooth="True")
    return line.render_embed()


# 访问限制装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" in session and "admin_id" in session:
            flash("online", "stat1")
            return f(*args, **kwargs)
        else:
            flash("offline", "stat2")
            return redirect(url_for("admin.login", next=request.url))

    return decorated_function


@admin.route("/", methods=['GET'])
@admin_login_req
def index():
    return render_template("admin/index.html", async_mode=socketio.async_mode, myechart=test_graph())


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
        flash("登录成功！", "ok")
        flash("online", "stat")
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout", methods=['GET'])
def logout():
    # session.pop("admin", None)
    # session.pop("admin_id", None)
    if '_flashes' in session:
        msg = session['_flashes']
        session.clear()
        session['_flashes'] = msg
    else:
        session.clear()
    flash("You've logged out.", "ok")
    return redirect(url_for('admin.login'))


@admin.route("/test/", methods=['GET', 'POST'])
@admin_login_req
def test():
    return render_template("admin/test.html")


@admin.route("/jstest/", methods=['GET'])
def jstest():
    return render_template("admin/jstest.html")


@admin.route("/account/<int:id>", methods=['GET', 'POST'])
@admin_login_req
def account(id=None):
    data = {}
    if id == None:
        id = int(session['admin_id'])
    try:
        admin = Admin.query.filter_by(account=session['admin']).first()
        last_adminlogin = admin.adminlogs[-1]
        data = {
            'name': admin.account,
            'last_login': last_adminlogin.addtime,
            'ip': last_adminlogin.ip
        }
    except BaseException as e:
        flash(e, "err")
    form1 = PwdForm()
    if form1.validate_on_submit():
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(form1.data['new_pwd'])
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for("admin.logout"))
    return render_template("admin/account.html", id=id, form1=form1, data=data)


@admin.route("/register", methods=['GET', 'POST'])
@admin_login_req
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        if 'face' not in data:
            face_name = 'default' + data['account'] + '.jpg'
            shutil.copy(app.config['MEM_DIR'] + 'default.jpg', app.config['MEM_DIR'] + face_name)
        if 'nickname' not in data:
            nickname = data['account']
        from werkzeug.security import generate_password_hash
        member = Member(
            account=data['account'],
            nickname=nickname,
            face=face_name,
            mobile=data['mobile'],
            pwd=generate_password_hash(data['pwd'])
        )
        try:
            db.session.add(member)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            flash("Error!", "err")
            return redirect(url_for("admin.memberlist", page=1))
        flash("添加成员成功", "ok")
        return redirect(url_for("admin.memberlist", page=1))
    return render_template("admin/register.html", form=form)


@admin.route("/memberlist/<int:page>", methods=['GET'])
@admin_login_req
def memberlist(page=None):
    if page == None:
        page = 1
    page_data = Member.query.order_by(
        Member.id
    ).paginate(page=page, per_page=5)
    return render_template("admin/memberlist.html", page_data=page_data)
