# coding:utf8
from app import db
from datetime import datetime

# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    account = db.Column(db.String(100), unique=True)  # 管理员帐号
    nickname = db.Column(db.String(100),unique=True)  # 管理员昵称
    pwd = db.Column(db.String(100))
    # is_super = db.Column(db.SmallInteger)
    # role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    # addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 添加时间
    # adminlogs = db.relationship("Adminlog", backref='admin')
    # oplogs = db.relationship("Oplog", backref='admin')


    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)