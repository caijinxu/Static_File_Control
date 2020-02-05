# -*- coding: utf-8 -*-
"""
create by caijinxu on 2019/4/3
"""
from flask import Blueprint
__author__ = 'caijinxu'


web = Blueprint('web', __name__, template_folder='templates')

from app.web import auth
from app.web import images
from app.web import index
from app.web import worker_config
from app.web import deadlinks
from app.web import api
from app.web import search
