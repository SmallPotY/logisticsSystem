# -*- coding:utf-8 -*-
from application import app, create_models
import www

if __name__ == '__main__':
    create_models(app)

    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler.start()
    # print('scheduler 启动')
    app.run(host=app.config['SERVER_HOST'], port=app.config['SERVER_PORT'])




#  nohup gunicorn -w4 -b 0.0.0.0:8000 manager:app --capture-output  &
