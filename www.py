# -*- coding:utf-8 -*-
from flask import render_template

from application import app
from web.controllers.admin import admin
from web.controllers.api import api

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')
