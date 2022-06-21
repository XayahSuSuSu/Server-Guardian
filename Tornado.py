import os
from abc import ABC

import tornado.ioloop
import tornado.web


class BaseHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class Check(BaseHandler, ABC):
    def get(self):
        self.write({
            'code': 1,
            'message': "",
        })


def make_app():
    return tornado.web.Application([
        (r'/api/v1/check', Check),
    ], static_path=os.path.join(os.path.dirname(__file__), "asserts"), static_url_prefix="/asserts/")


if __name__ == "__main__":
    # 判断是否存在asserts文件夹，没有则创建
    if not os.path.exists("asserts"):
        os.mkdir("asserts")
    app = make_app()
    app.listen(port=3399)
    tornado.ioloop.IOLoop.current().start()
