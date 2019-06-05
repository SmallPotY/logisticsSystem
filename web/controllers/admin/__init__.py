# -*- coding:utf-8 -*-
from flask import Blueprint

admin = Blueprint('admin', __name__)

from web.controllers.admin.member.vUser import *

from web.controllers.admin.expressDelivery.vExpressInfo import *
