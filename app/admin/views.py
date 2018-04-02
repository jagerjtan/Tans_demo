# coding: utf8
from . import admin
from flask import render_template, url_for, redirect, flash, request, session

@admin.route("/",methods=['GET'])
def index():
    return render_template("admin/index.html")

