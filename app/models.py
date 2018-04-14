# coding:utf8
from app import db
from datetime import datetime


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    account = db.Column(db.String(100), unique=True)  # 管理员帐号
    nickname = db.Column(db.String(100), unique=True)  # 管理员昵称
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship("Adminlog", backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.account

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 会员
class Member(db.Model):
    __tablename__ = "member"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    account = db.Column(db.String(100), unique=True)
    nickname = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    mobile = db.Column(db.String(11), unique=True)  # 手机
    info = db.Column(db.String(100))  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    birthday = db.Column(db.DateTime)  # 出生日期

    memberlogs = db.relationship('Memberlog', backref='member')  # 成员日志外键关系关联
    dailylogs = db.relationship('DailyLog', backref='member')  # 成员账户记录外键关联

    def __repr__(self):
        return "<Member %r>" % self.account

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员登录日志：
class Memberlog(db.Model):
    __tablename__ = "memberlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 最近登录时间

    def __repr__(self):
        return "<Memberlog %r>" % self.id


class Home(db.Model):
    __tablename__ = "home"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    account = db.Column(db.String(100), unique=True)  # 标识号
    nickname = db.Column(db.String(100), unique=True)  # 标识号别名
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间

    net_asset = db.Column(db.Float)  # 总资产
    debt = db.Column(db.Float)  # 债务
    cash = db.Column(db.Float)  # 现金
    asset = db.Column(db.Float)  # 资产

    homelogs = db.relationship('Homelog', backref='home')  # Home日志外键关系关联

    def __repr__(self):
        return "<Home %r>" % self.account


class Homelog(db.Model):
    __tablename__ = "homelog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    home_id = db.Column(db.Integer, db.ForeignKey('home.id'))  # 所述home
    ip = db.Column(db.String(100))  # 位置
    edit_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 修改时间
    edit_log = db.Column(db.Text)  # 修改内容

    def __repr__(self):
        return "<Home %r>" % self.id


class DailyLog(db.Model):
    __tablename__ = "dailylog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    uuid = db.Column(db.String(100), unique=True)  # 唯一标识符
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    type = db.Column(db.String(20))  # 类型 (收入/支出)
    amount = db.Column(db.Float)  # 数额
    category = db.Column(db.String(100))  # 所属项目
    status = db.Column(db.String(100))  # 状态
    content = db.Column(db.Text)  # 备注
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))  # 所属成员外键
    test = db.Column(db.Integer)

    def __repr__(self):
        return "<DailyLog %r>" % self.id
