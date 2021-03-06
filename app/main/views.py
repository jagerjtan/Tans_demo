# coding: utf8
from . import main
from app import db, app
from flask import render_template, url_for, redirect, flash, request, session
from app.main.forms import LoginForm, PwdForm, AddHomeForm, IssueDailyLogForm, AccountEditForm
from app.models import Member, Memberlog, Home, DailyLog
from app.decorators import member_login_req
import uuid, os, datetime
from werkzeug.utils import secure_filename


def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@main.route("/", methods=['GET'])
@member_login_req
def home():
    return redirect(url_for("main.index", page=1))


@main.route("/<int:page>/", methods=['GET'])
@member_login_req
def index(page=None):
    if page is None:
        page = 1
    logs = DailyLog.query.order_by(
        DailyLog.addtime.desc()
    ).paginate(page=page, per_page=10)
    for item in logs.items:
        with db.session.no_autoflush:
            item.member_id = Member.query.filter_by(id=item.member_id).first().nickname

    today = datetime.datetime.now()
    costlist, incomelist = [], []
    for item in logs.items:
        if item.addtime.date() == today.date():
            costlist.append(item.amount if item.type == '支出' else 0)
            incomelist.append(item.amount if item.type == '收入' else 0)

    data = {'today':today.strftime("%Y-%m-%d %A"), 'income': sum(incomelist), 'cost': sum(costlist)}
    return render_template("main/index.html", logs=logs, data=data)


@main.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if "member" in session and "member_id" in session:
        flash("你已登录，请不要重复登录", "err")
        return redirect(request.args.get("next") or url_for("main.home"))
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
        return redirect(request.args.get("next") or url_for("main.home"))
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


@main.route("/account/<int:id>", methods=['GET', 'POST'])
@member_login_req
def account(id=None):
    data = {}
    if id == None:
        id = int(session['member_id'])
    try:
        member = Member.query.filter_by(account=session['member']).first()
        last_memberlogin = member.memberlogs[-1]
        data = {
            'nickname': member.nickname,
            'last_login': last_memberlogin.addtime,
            'ip': last_memberlogin.ip,
            'face': member.face
        }
        dailylogs = [*member.dailylogs]
        dailylogs.reverse()

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
    return render_template("main/account.html", id=id, form1=form1, data=data, dailylogs=dailylogs)


@main.route("/account_edit/<int:id>", methods=['GET', 'POST'])
@member_login_req
def account_edit(id):
    member = Member.query.get_or_404(int(id))
    form = AccountEditForm()
    # form.face.validators=[]
    if request.method == 'GET':
        form.nickname.data = member.nickname
        form.mobile.data = member.mobile
        form.birthday.data = member.birthday
        form.info.data = member.info
    if form.validate_on_submit():
        data = form.data

        if form.face.data:
            file_url = secure_filename(form.face.data.filename)
            oldface = member.face
            member.face = change_filename(file_url)
            form.face.data.save(app.config['MEM_DIR'] + member.face)

        member.nickname = data['nickname']
        member.mobile = data['mobile']
        member.info = data['info']
        member.birthday = data['birthday']

        try:
            db.session.add(member)
            db.session.commit()
        except BaseException:
            db.session.roll()
            flash("Errors!", "err")
            return redirect(url_for("main.account_eidt", id=id))
        flash("Edit done", "ok")
        os.renames(app.config['MEM_DIR']+oldface, app.config['MEM_DIR']+'abandoned-'+oldface)
        return redirect(url_for("main.account", id=id))
    return render_template("main/account_edit.html", form=form, id=id)


@main.route("/database/", methods=['GET', 'POST'])
@member_login_req
def database():
    form = AddHomeForm()
    home = Home.query.order_by(Home.id.desc()).first()
    from app.charts import home_basic
    homechart = home_basic(home)

    if form.validate_on_submit():
        data = form.data
        new_home = Home(
            account=data['account'],
            nickname=data['nickname'],
            net_asset=data['net_asset'],
            asset=data['asset'],
            debt=data['debt'],
            cash=data['cash']
        )
        try:
            db.session.add(new_home)
            db.session.commit()
        except BaseException:
            db.session.rollback()
            flash("Error", "err")
            return redirect(url_for('main.database'))
        flash("Add Home Success", "ok")
        return redirect(url_for("main.database"))
    return render_template("main/database.html", form=form, myechart=homechart)


@main.route("/issueclaim", methods=['GET', 'POST'])
@member_login_req
def issueclaim():
    form = IssueDailyLogForm()
    cateset = ["食物", "杂费", "家居", "传统", "节庆", "车辆", "出行",
               "健康", "消费", "宠物", "旅游", "其他", "亲戚", "其他"]
    sets = [(x, x) for x in cateset]
    form.category.choices = sets
    subsets = [_ for _ in form.category]
    if form.validate_on_submit():
        data = form.data
        dailylog = DailyLog(
            uuid=uuid.uuid4().hex,
            type='支出',
            category=data['category'],
            amount=data['amount'],
            member_id=session['member_id'],
            content=data['content'],
            status='pending'
        )
        try:
            db.session.add(dailylog)
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            flash("出错了!请重试!", "err")
            return redirect(url_for("main.issueclaim"))
        flash("添加成功", "ok")
        return redirect(url_for("main.home"))
    return render_template("main/issueclaim.html", form=form, subsets=subsets)


@main.route("/issueincome/", methods=['GET', 'POST'])
@member_login_req
def issueincome():
    form = IssueDailyLogForm()
    sets = [("月度剩余", "月度剩余"), ("工资转入", "工资转入"), ("企业转入", "企业转入")]
    form.category.choices = sets
    subsets = [_ for _ in form.category]
    if form.validate_on_submit():
        data = form.data
        dailylog = DailyLog(
            uuid=uuid.uuid4().hex,
            type="收入",
            category=data['category'],
            amount=data['amount'],
            member_id=session['member_id'],
            content=data['content'],
            status='pending'
        )
        try:
            db.session.add(dailylog)
            db.session.commit()
        except BaseException as e:
            print(e)
            db.session.rollback()
            flash("出错了!请重试!", "err")
            return redirect(url_for("main.issueincome"))
        flash("添加成功", "ok")
        return redirect(url_for("main.home"))
    return render_template("main/issueincome.html", form=form, subsets=subsets)


@main.route("/memberlist/<int:page>/", methods=['GET', 'POST'])
@member_login_req
def memberlist(page=None):
    if page == None:
        page = 1
    page_data = Member.query.order_by(
        Member.id
    ).paginate(page=page, per_page=6)
    return render_template('main/memberlist.html', page_data=page_data)


@main.route("/memberdetail/<int:id>/", methods=['GET', 'POST'])
@member_login_req
def memberdetail(id=None):
    if id == None:
        id = 1
    member = Member.query.filter_by(id=id).first()
    member.pwd = ""
    return render_template('main/memberdetail.html', id=id, member=member)


@main.route("/log_detail/<int:id>", methods=['GET'])
@member_login_req
def log_detail(id=None):
    if id == None:
        id = 1
    log = DailyLog.query.filter_by(id=id).first()
    log.test = Member.query.filter_by(id=log.member_id).first().nickname
    return render_template("main/log_detail.html", id=id, log=log)


@main.route("/log_del/<int:id>/", methods=['GET'])
@member_login_req
def log_del(id=None):
    auth = DailyLog.query.filter_by(id=id).first().member_id
    if id == None:
        flash("错误链接", "err")
        return redirect(url_for("main.home"))
    elif session['member_id'] != auth:
        flash("你没有权限", "err")
        return redirect(url_for("main.home"))
    flash("ok", "ok")
    return redirect(url_for("main.home"))
