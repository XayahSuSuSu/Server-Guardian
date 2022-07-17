import hashlib
import os

import tornado.gen
import tornado.ioloop
import tornado.web

from router.routes import routes
from util import db


def make_app():
    return tornado.web.Application(routes, static_path=os.path.join(os.path.dirname(__file__), "asserts"),
                                   static_url_prefix="/asserts/")


if __name__ == "__main__":
    # 初始化MySQL数据库
    db.init()
    if len(db.get_all('account')) == 0:
        username = 'admin'
        password = hashlib.md5(username.encode('utf8')).hexdigest()
        db.insert('account', [username, password])
    # 判断是否存在asserts文件夹，没有则创建
    if not os.path.exists("asserts"):
        os.mkdir("asserts")
    if not os.path.exists("asserts/devices"):
        os.mkdir("asserts/devices")
    if not os.path.exists("asserts/authorize"):
        os.mkdir("asserts/authorize")
    app = make_app()
    app.listen(port=33307)
    tornado.ioloop.IOLoop.current().start()
