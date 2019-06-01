# -*- coding:utf-8 -*-
from flask import render_template

from application import app
# from web.controllers.express import ex
from web.controllers.api import api

# app.register_blueprint(ex, url_prefix='/ex')
app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    return render_template('index.html')
