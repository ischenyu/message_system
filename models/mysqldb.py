'''
editor:ischenyu.
'''

import hashlib
import logging
import pymysql
import redis
import time

# 打开数据库连接
db = pymysql.connect(host='192.168.1.2',
                     user='root',
                     password='Dingtalk1234561017',
                     database='python')
timestamp = lambda: int(time.time())

# 初始化 Redis 连接和连接池
redis_pool = redis.ConnectionPool(host='192.168.1.2', port=6379, db=10, password='Dingtalk1234561017')
redis_client = redis.Redis(connection_pool=redis_pool)
# 初始化日志记录器
logging.basicConfig(level=logging.ERROR)  # 设置日志级别为 ERROR 或更高级别


def close_connections():
    try:
        if db.open:
            db.close()
        redis_pool.disconnect()
    except Exception as e:
        logging.error("An error occurred while closing connections: %s", e)


def User_signup(username, password, email):
    init_time = int(time.time())
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor = db.cursor()
    try:
        # 检查用户是否存在，使用参数化查询以防止 SQL 注入攻击
        sql_test = "SELECT * FROM python.user WHERE username=%s"
        cursor.execute(sql_test, (username,))
        if cursor.rowcount > 0:
            return 114
        sql = "INSERT INTO python.user(username, password, email, init_time) VALUES (%s, %s, %s, %s)"
        # 执行插入操作，使用参数化查询以防止 SQL 注入攻击
        cursor.execute(sql, (username, password_hash, email, init_time))
        # 提交事务并关闭游标
        db.commit()
        return True
    except Exception as e:
        logging.error("An error occurred during user signup: %s", e)
        # 回滚事务并关闭游标
        db.rollback()
        return False
    finally:
        cursor.close()


def User_login(username, password):
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cached_user = redis_client.get(username)
        if cached_user:
            return True
        sql = "SELECT * FROM python.user WHERE username=%s AND password=%s"
        with db.cursor() as cursor:
            cursor.execute(sql, (username, password_hash))
            results = cursor.fetchall()
            if len(results) == 0:
                return False
            else:
                with redis_client.pipeline() as pipe:
                    pipe.setex(username, 3600, 'authenticated')
                    pipe.execute()
                return True
    except Exception as e:
        logging.error("An error occurred while user login: %s", e)
        return 'error'

    finally:
        close_connections()


def User_forget(email, password):
    password = hashlib.sha256(password.encode()).hexdigest()
    # 判断用户邮箱是否存在
    sql_user_init = """SELECT * FROM python.user WHERE email='%s'""" % (email)
    cursor = db.cursor()
    try:
        cursor.execute(sql_user_init)
        if cursor.rowcount == 0:
            return 'user_not_exist'
        else:
            # 修改对应用户的密码
            sql = """UPDATE python.user SET password='%s' WHERE email='%s'""" % (password, email)
            # 使用cursor()方法获取操作游标
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                db.close()
                return True
            except Exception as e:
                logging.error("An error occurred during user signup: %s", e)
                # 回滚事务并关闭游标
                db.rollback()
                return 500
    except Exception as e:
        logging.error("An error occurred during user signup: %s", e)
        # 回滚事务并关闭游标
        db.rollback()
        return 500
    finally:
        cursor.close()


def User_info(username):
    sql = """SELECT * FROM python.user WHERE username='%s'""" % username
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) == 0:
            return False
        else:
            return results[0]
    except:
        return 'error'
