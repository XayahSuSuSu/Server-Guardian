import datetime

import pymysql

HOST = '127.0.0.1'  # 宿主机地址
PORT = 33306  # 宿主机地址
USER = 'root'  # 用户名
PASSWORD = '123456'  # 密码
DB = 'App'  # 数据库名
global db

TABLE_DATA = 'data'  # 数据表名
FIELD_DATA = [
    "state text,",
    "battery_car text,",
    "battery_drone text",
]  # 字段

TABLE_ACTION = 'action'  # 操作表名
FIELD_ACTION = [
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
    "device_code text",
]  # 字段


def timestamp():
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
    # 创建表(DATA)
    field_data = "".join(FIELD_DATA)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS {}(id int primary key not null auto_increment,".format(TABLE_DATA)
        + "created_at timestamp,updated_at timestamp,"
        + field_data
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


def insert(table, data):
    """插入一条记录"""
    db.ping()
    cursor = db.cursor()
    cursor.execute("use {};".format(DB))
    insert_data = "INSERT INTO {} VALUES (0,'{}','{}'".format(table, timestamp(), timestamp())
    for i in data:
        insert_data += ",'"
        insert_data += i
        insert_data += "'"
    insert_data += ")"
    cursor.execute(insert_data)
    db.commit()


def update(table, item_id, data_name, data):
    """更新一条记录"""
    db.ping()
    cursor = db.cursor()
    cursor.execute("use {};".format(DB))
    cursor.execute(
        "update {} set {} = '{}',updated_at = '{}' where id = {}".format(table, data_name, data, timestamp(), item_id))
    db.commit()
