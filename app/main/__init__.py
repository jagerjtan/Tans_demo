# coding:utf8
from flask import Blueprint

main = Blueprint("main", __name__)

import app.main.views
