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
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    adminlogs = db.relationship("Adminlog", backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 登录时间

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
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识符
    birthday = db.Column(db.DateTime) #出生日期

    memberlogs = db.relationship('Memberlog', backref='member')  # 会员日志外键关系关联

    def __repr__(self):
        return "<Member %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员登录日志：
class Memberlog(db.Model):
    __tablename__ = "memberlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 最近登录时间

    def __repr__(self):
        return "<Memberlog %r>" % self.id
