import json
import os
from abc import ABC

import tornado.ioloop
import tornado.web

from util import db


class BaseHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class Check(BaseHandler, ABC):
    def get(self):
        self.write(json.dumps({
            'code': 1,
            'msg': '操作成功！',
            'data': {}
        }, ensure_ascii=False))


class AppData(BaseHandler, ABC):
    def get(self):
        data = db.get_all('data')[0]
        self.write(json.dumps({
            'code': 1,
            'msg': '操作成功！',
            'data': {
                'state': data['state'],
                'battery_car': data['battery_car'],
                'battery_drone': data['battery_drone']
            }
        }, ensure_ascii=False))

    def post(self):
        data = db.get_all('data')[0]
        state = data['state']
        battery_car = data['battery_car']
        battery_drone = data['battery_drone']
        body_arguments = self.request.body_arguments
        if 'state' in body_arguments:
            state = body_arguments['state'][0].decode()
        if 'battery_car' in body_arguments:
            battery_car = body_arguments['battery_car'][0].decode()
        if 'battery_drone' in body_arguments:
            battery_drone = body_arguments['battery_drone'][0].decode()
        db.update('data', 1, 'state', state)
        db.update('data', 1, 'battery_car', battery_car)
        db.update('data', 1, 'battery_drone', battery_drone)
        self.write(json.dumps({
            'code': 1,
            'msg': '操作成功！',
            'data': {
                'state': state,
                'battery_car': battery_car,
                'battery_drone': battery_drone
            }
        }, ensure_ascii=False))


def make_app():
    return tornado.web.Application([
        (r'/api/v1/check', Check),
        (r'/api/v1/app/data', AppData),
    ], static_path=os.path.join(os.path.dirname(__file__), "asserts"), static_url_prefix="/asserts/")


if __name__ == "__main__":
    # 初始化MySQL数据库
    db.init()
    if len(db.get_all('data')) == 0:
        db.insert('data', ['', '', ''])
    # 判断是否存在asserts文件夹，没有则创建
    if not os.path.exists("asserts"):
        os.mkdir("asserts")
    app = make_app()
    app.listen(port=33307)
    tornado.ioloop.IOLoop.current().start()
