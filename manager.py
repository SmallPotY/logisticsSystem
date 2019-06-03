# -*- coding:utf-8 -*-
from application import app, create_models
import www
from flask_apscheduler import APScheduler

if __name__ == '__main__':
    create_models(app)

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])
