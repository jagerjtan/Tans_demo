# coding: utf8
from . import main
from flask import render_template, url_for, redirect, flash, request, session

@main.route("/",methods=['GET'])
def index():
    return render_template("main/index.html")