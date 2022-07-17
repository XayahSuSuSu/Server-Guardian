import hashlib
import json
import threading
import time
from abc import ABC
from concurrent.futures import ThreadPoolExecutor

import qrcode
import tornado.gen
import tornado.web
from tornado.concurrent import run_on_executor

from util import db

CODE_SUCCESS = 1
MSG_SUCCESS = '操作成功'
MSG_LOGIN_SUCCESS = '登录成功'

CODE_FAILED = -1
MSG_LOGIN_FAILED = '登录失败，请检查用户名或密码'
MSG_PARA_LOSS = '参数丢失或不正确'


def ret(code, msg, data):
    return {
        'code': code,
        'msg': msg,
        'data': data
    }


class BaseHandler(tornado.web.RequestHandler, ABC):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class Check(BaseHandler, ABC):
    def get(self):
        self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {}), ensure_ascii=False))


class Login(BaseHandler, ABC):
    def post(self):
        body_arguments = self.request.body_arguments
        if 'username' in body_arguments and 'password' in body_arguments:
            para_username = body_arguments['username'][0].decode()
            para_password = body_arguments['password'][0].decode()
            for i in db.get_all('account'):
                if i['username'] == para_username:
                    if i['password'] == para_password:
                        self.write(json.dumps(ret(CODE_SUCCESS, MSG_LOGIN_SUCCESS, {}), ensure_ascii=False))
                        return
        self.write(json.dumps(ret(CODE_FAILED, MSG_LOGIN_FAILED, {}), ensure_ascii=False))


semaphore = threading.Semaphore(0)
action_list = []


class Action(tornado.web.RequestHandler, ABC):
    executor = ThreadPoolExecutor(2)

    @tornado.gen.coroutine
    def get(self):
        yield self.sem()
        if len(action_list) != 0:
            action_dic = action_list.pop()
            print("Action", "get", action_dic)
            db.insert('action', [action_dic['action'], 'finished'])
            self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, action_dic), ensure_ascii=False))
            return
        self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {}), ensure_ascii=False))

    @run_on_executor
    def sem(self):
        semaphore.acquire()
        return

    def post(self):
        body_arguments = self.request.body_arguments
        if 'action' in body_arguments:
            action = body_arguments['action'][0].decode()
            action_dic = {
                'action': action,
                'state': ''
            }
            print("Action", "post", action_dic)
            if len(action_list) != 0:
                action_list.clear()
            else:
                semaphore.release()
            action_list.append(action_dic)
            self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, action_dic), ensure_ascii=False))
            return
        self.write(json.dumps(ret(CODE_FAILED, MSG_PARA_LOSS, {}), ensure_ascii=False))


class State(BaseHandler, ABC):
    def get(self):
        para_device_code = self.get_query_arguments('device_code')
        if len(para_device_code) != 0:
            data = db.get_all('state')
            state = {
                'device_code': '',
                'state': '',
                'battery_car': '',
                'battery_drone': '',
            }
            for i in data:
                if i['device_code'] == para_device_code[0]:
                    state = i
            self.write(json.dumps(
                ret(CODE_SUCCESS, MSG_SUCCESS, {
                    'device_code': state['device_code'],
                    'state': state['state'],
                    'battery_car': state['battery_car'],
                    'battery_drone': state['battery_drone']
                }), ensure_ascii=False))
            return
        self.write(json.dumps(ret(CODE_FAILED, MSG_PARA_LOSS, {}), ensure_ascii=False))

    def post(self):
        body_arguments = self.request.body_arguments
        if 'device_code' in body_arguments:
            para_device_code = body_arguments['device_code'][0].decode()
            data = {
                'device_code': '',
                'state': '',
                'battery_car': '',
                'battery_drone': '',
            }
            for i in db.get_all('state'):
                if i['device_code'] == para_device_code:
                    data = i
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
            db.update_by_field('state', 'device_code', para_device_code, 'state', state)
            db.update_by_field('state', 'device_code', para_device_code, 'battery_car', battery_car)
            db.update_by_field('state', 'device_code', para_device_code, 'battery_drone', battery_drone)
            self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {
                'device_code': para_device_code,
                'state': state,
                'battery_car': battery_car,
                'battery_drone': battery_drone
            }), ensure_ascii=False))
            return
        self.write(json.dumps(ret(CODE_FAILED, MSG_PARA_LOSS, {}), ensure_ascii=False))


class Authorize(BaseHandler, ABC):
    def get(self):
        para_id = self.get_query_arguments('id')
        if len(para_id) == 0:
            db.insert('authorize', [''])
            authorize_id = db.get_all('authorize')[-1]['id']
            img = qrcode.make(json.dumps({
                'id': authorize_id
            }))
            asserts = "asserts/authorize/qrcode_{}.png".format(authorize_id)
            img.save(asserts)
            self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {
                'id': authorize_id,
                'url': asserts
            }), ensure_ascii=False))
        else:
            authorize_id = db.get_all('authorize')
            dic = {
                'id': '',
                'device_code': ''
            }
            for i in authorize_id:
                if str(i['id']) == para_id[0]:
                    dic = i
            self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {
                'id': dic['id'],
                'device_code': dic['device_code']
            }), ensure_ascii=False))

    def post(self):
        body_arguments = self.request.body_arguments
        if 'id' in body_arguments and 'device_code' in body_arguments:
            authorize_id = body_arguments['id'][0].decode()
            device_code = body_arguments['device_code'][0].decode()
            db.update_by_id('authorize', authorize_id, 'device_code', device_code)
            self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {}), ensure_ascii=False))
        self.write(json.dumps(ret(CODE_FAILED, MSG_PARA_LOSS, {}), ensure_ascii=False))


class Device(BaseHandler, ABC):
    def get(self):
        devices = db.get_all('device')
        print(devices)
        dic = []
        for i in devices:
            dic.append({
                'id': i['id'],
                'factory_date': i['factory_date'].strftime("%Y-%m-%d %H:%M:%S"),
                'device_code': i['device_code'],
                'bind_state': i['bind_state'],
                'qrcode_path': i['qrcode_path'],
            })
        self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, dic), ensure_ascii=False))

    def post(self):
        body_arguments = self.request.body_arguments
        if 'bind_state' in body_arguments and 'device_code' in body_arguments:
            bind_state = body_arguments['bind_state'][0].decode()
            device_code = body_arguments['device_code'][0].decode()
            db.update_by_field('device', 'device_code', device_code, 'bind_state', bind_state)
        else:
            db_timestamp = db.db_timestamp()
            timestamp = time.mktime(time.strptime(db_timestamp, "%Y-%m-%d %H:%M:%S"))
            device_code = hashlib.md5(str(timestamp).encode('utf8')).hexdigest()
            img = qrcode.make(json.dumps({
                'device_code': device_code
            }))
            asserts = "asserts/devices/qrcode_{}.png".format(timestamp)
            img.save(asserts)
            db.insert('device', [db_timestamp, device_code, '否', asserts])
            db.insert('state', [device_code, '', '', ''])
        self.write(json.dumps(ret(CODE_SUCCESS, MSG_SUCCESS, {}), ensure_ascii=False))


routes = [
    (r'/api/v1/check', Check),
    (r'/api/v1/state', State),
    (r'/api/v1/action', Action),
    (r'/api/v1/login', Login),
    (r'/api/v1/authorize', Authorize),
    (r'/api/v1/device', Device),
]