# -*- coding:utf-8 -*-
from flask import Blueprint

api = Blueprint('api', __name__)

from web.controllers.api.logisticsTracking.vExpressInformation import *


