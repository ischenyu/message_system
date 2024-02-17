'''
editor:ischenyu.
ToDo:优化请求函数,防止重复请求及SQL注入.
'''


import pymysql, time, hashlib, redis, logging

# 打开数据库连接
db = pymysql.connect(host='192.168.1.15',
                     user='root',
                     password='Dingtalk1234561017',
                     database='python')
timestamp = lambda: int(time.time())

# 初始化 Redis 连接和连接池
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=10)
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
    init_time = timestamp()
    password = hashlib.sha256(password.encode()).hexdigest()
    sql = """INSERT INTO python.user(username, password, email, init_time)
      VALUES ('%s', '%s', '%s', '%s')""" % (username, password, email, init_time)
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        db.close()
        return True
    except:
        # 发生错误时回滚
        db.rollback()
        db.close()
        return False
    finally:
        del username
        del password
    
def User_login(username, password):
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # 尝试从缓存中获取用户信息
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
                # 将用户信息缓存到 Redis 中，有效期设置为一定时间
                with redis_client.pipeline() as pipe:
                    pipe.setex(username, 3600, 'authenticated')
                    pipe.execute()
                return True
    
    except Exception as e:
        logging.error("An error occurred: %s", e)
        return 'error'
    finally:
        close_connections()
    
def User_forget(username, password):
    password = hashlib.sha256(password.encode()).hexdigest()
    # 修改对应用户的密码
    sql = """UPDATE python.user SET password='%s' WHERE username='%s'""" % (password, username)
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        db.close()
        return True
    except:
        return 'error'
    
def User_info(username):
    sql = """SELECT * FROM python.user WHERE username='%s'""" % (username)
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