import datetime

import pymysql

HOST = '127.0.0.1'  # 宿主机地址
PORT = 33306  # 宿主机地址
USER = 'root'  # 用户名
PASSWORD = '123456'  # 密码
DB = 'App'  # 数据库名
global db

TABLE_STATE = 'state'  # 状态表名
FIELD_STATE = [
    "device_code text,",
    "state text,",
    "battery_car text,",
    "battery_drone text",
]  # 字段

TABLE_ACTION = 'action'  # 操作表名
FIELD_ACTION = [
    "device_code text,",
    "action text,",
    "state text",
]  # 字段

TABLE_ACCOUNT = 'account'  # 账户表名
FIELD_ACCOUNT = [
    "username text,",
    "password text",
]  # 字段

TABLE_AUTHORIZE = 'authorize'  # 授权表名
FIELD_AUTHORIZE = [
    "device_code text,",
    "rtmp_address_court text,",
    "rtmp_address_car text",
]  # 字段

TABLE_DEVICE = 'device'  # 设备表名
FIELD_DEVICE = [
    "factory_date timestamp,",
    "device_code text,",
    "bind_state text,",
    "qrcode_path text",
]  # 字段

TABLE_FACE = 'face'
FIELD_FACE = [
    "device_code text,",
    "name text,",
    "path text,",
    "face_feature mediumblob",
]


def db_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_all(table):
    """返回表中所有数据"""
    db.ping()
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("use {};".format(DB))
    cursor.execute("SELECT * from {}".format(table))
    data = cursor.fetchall()
    db.commit()
    return data


def init():
    """创建数据库和数据表"""
    global db
    db = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, charset='utf8')
    db.ping()
    cursor = db.cursor()
    # 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARSET utf8 COLLATE utf8_general_ci;".format(DB))
    # 选择数据库
    cursor.execute("use {};".format(DB))
    # 创建表(STATE)
    field_state = "".join(FIELD_STATE)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_STATE)
        + "created_at timestamp,updated_at timestamp,"
        + field_state
        + ");")

    # 创建表(ACTION)
    field_action = "".join(FIELD_ACTION)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_ACTION)
        + "created_at timestamp,updated_at timestamp,"
        + field_action
        + ");")

    # 创建表(ACCOUNT)
    field_account = "".join(FIELD_ACCOUNT)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_ACCOUNT)
        + "created_at timestamp,updated_at timestamp,"
        + field_account
        + ");")

    # 创建表(AUTHORIZE)
    field_authorize = "".join(FIELD_AUTHORIZE)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_AUTHORIZE)
        + "created_at timestamp,updated_at timestamp,"
        + field_authorize
        + ");")

    # 创建表(DEVICE)
    field_device = "".join(FIELD_DEVICE)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_DEVICE)
        + "created_at timestamp,updated_at timestamp,"
        + field_device
        + ");")

    # 创建表(FACE)
    field_face = "".join(FIELD_FACE)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_FACE)
        + "created_at timestamp,updated_at timestamp,"
        + field_face
        + ");")


def insert(table, data):
    """插入一条记录"""
    db.ping()
    cursor = db.cursor()
    cursor.execute("use {};".format(DB))
    insert_data = "INSERT INTO {} VALUES (0,'{}','{}'".format(table, db_timestamp(), db_timestamp())
    for i in data:
        insert_data += ",%s"
    insert_data += ")"
    cursor.execute(insert_data, tuple(data))
    db.commit()


def update_by_id(table, item_id, data_name, data):
    """更新一条记录"""
    db.ping()
    cursor = db.cursor()
    cursor.execute("use {};".format(DB))
    cursor.execute(
        "update {} set {} = '{}',updated_at = '{}' where id = {}".format(table, data_name, data, db_timestamp(),
                                                                         item_id))
    db.commit()


def update_by_field(table, field_name, field_data, data_name, data):
    """更新一条记录"""
    db.ping()
    cursor = db.cursor()
    cursor.execute("use {};".format(DB))
    cursor.execute(
        "update {} set {} = '{}',updated_at = '{}' where {} = '{}'".format(table, data_name, data, db_timestamp(),
                                                                           field_name, field_data))
    db.commit()
