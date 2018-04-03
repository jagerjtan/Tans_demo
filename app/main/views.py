# coding: utf8
from . import main
from flask import render_template, url_for, redirect, flash, request, session

@main.route("/",methods=['GET'])
def index():
    return render_template("main/index.html")

@main.route("/userlogin/",methods=['GET','POST'])
def login():
    return render_template("main/login.html")

@main.route("/logout",methods=['GET'])
def logout():
    return redirect(url_for('main.login'))

@main.route("/pwd/",methods=['GET','POST'])
def pwd():
    return render_template("main/pwd.html")

@main.route("/account/",methods=['GET'])
def account():
    return render_template("main/account.html")