import random
import time

from functools import wraps
from collections import defaultdict
from flask import Flask, make_response, render_template, request, jsonify, url_for, redirect
from itsdangerous import URLSafeSerializer

from models import email_captcha
from models import mysqldb

app = Flask(__name__, static_folder='static')
app.secret_key = 'cookie_key'  # 设置一个用于签名的秘钥
# 创建一个序列化器对象
serializer = URLSafeSerializer(app.secret_key)
app.config['SECRET_KEY'] = 'your_secret_key'

# 用于存储每个IP地址的请求时间戳
request_history = defaultdict(list)
REQUEST_LIMIT = 3  # 每分钟允许的请求数
TIME_WINDOW = 60  # 时间窗口为60秒


def rate_limit_exceeded(ip):
    current_time = time.time()
    # 移除时间窗口之外的请求时间戳
    request_history[ip] = [t for t in request_history[ip] if t > current_time - TIME_WINDOW]
    return len(request_history[ip]) > REQUEST_LIMIT


def rate_limited(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        if rate_limit_exceeded(ip):
            return jsonify({'error': 'Rate limit exceeded. Try again later.', 'code': 429})
        request_history[ip].append(time.time())
        return func(*args, **kwargs)

    return decorated_function


@app.route("/")
def index():
    try:
        logining = request.cookies.get('logining')
        user_email = request.cookies.get('user_email')
        if logining == 'True':
            return render_template("index.html", logined=True, email=user_email)
        else:
            return render_template("index.html", logined=False)
    except AttributeError:
        return render_template("index.html")


@app.route("/messages", methods=['GET'])
def get_messages():
    messages = mysqldb.get_message()
    return jsonify({
        "code": 0,
        "msg": "获取消息成功",
        "data": messages
    })


@app.route('/logout', methods=['GET'])
def logout():
    if request.cookies.get('logining') == 'True':
        # 更新cookie'logining'的值为False.
        max_age = 604800
        # 加密用户信息并设置到 Cookie 中
        resp = make_response(jsonify({"success": True, "message": "退出成功", 'code': 200}))
        resp.set_cookie('user_email', max_age=max_age)
        resp.set_cookie('logining', str(False), max_age=max_age)
        # return resp
        return redirect('/')
    else:
        return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        # 获取传回的数据
        data = request.get_json()
        print(data)
        email = data['email']
        input_code = data['vercode']
        # print(email, input_code)
        password = data['password']
        username = data['username']
        if data['agreement'] == 'on':
            try:
                if email_captcha.verify_code(email, input_code):
                    if mysqldb.user_signup(username, password, email):
                        return jsonify({"code": 200, "success": True, "message": "注册成功"})
                    elif mysqldb.user_signup(username, password, email) == 114:
                        return jsonify({"code": 402, "success": False, "message": "注册失败,用户已存在"})
                    else:
                        return jsonify(
                            {"code": 500, "success": False, "message": "注册失败,数据库错误,请联系管理员解决"}), 401
                else:
                    return jsonify({"message": "验证码错误"}), 401
            except NameError as e:
                print(e)
                return jsonify({"success": False, "message": "验证码错误NameError"})
            except Exception as e:
                print(e)
                return jsonify({"success": False, "message": "验证码错误Exception"})
        else:
            return jsonify({"success": False, "message": "请同意协议"}), 400
    elif request.method == 'GET':
        return render_template("register.html")


@app.route('/login', methods=['POST', 'GET'])
@rate_limited
def api_login():
    if request.method == 'POST':
        try:
            # 获取传回的数据
            data = request.get_json()
            username = data['username']
            email = data['username']
            password = data['password']
            if mysqldb.user_login(username, password):
                # 用户信息写入数据库，注册成功后写入cookie，重定向到主页.
                max_age = 604800
                # 加密用户信息并设置到 Cookie 中
                encrypted_email = serializer.dumps(email)
                resp = make_response(jsonify({"success": True, "message": "登录成功", 'code': 200}))
                resp.set_cookie('user_email', encrypted_email, max_age=max_age)
                resp.set_cookie('logining', str(True), max_age=max_age)
                return resp
            elif mysqldb.user_login(username, password) == 'error':
                return jsonify({"message": "服务器内部错误"}), 500
            else:
                return jsonify({"code": 401, "message": "用户名或密码错误"})
        except KeyError:
            return jsonify({"code": 400, "message": "回调数据不完整！"}), 400
    elif request.method == 'GET':
        try:
            # 从请求的 cookie 中获取名为 'user_email' 的值
            logining = request.cookies.get('logining')
            if logining == 'True':
                # 执行重定向
                return redirect(url_for('index'))
            else:
                return render_template('login.html')
        except AttributeError:
            return render_template('login.html')


# 记录用户最近一次请求验证码的时间
last_request_time = {}


@app.route('/register/captcha', methods=['POST', 'GET'])
def captcha():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        print(email)
        if not email:
            return jsonify({"success": False, 'message': 'Email is required', 'code': 400})

        # 检查是否已经记录了用户的最近一次请求时间
        if email in last_request_time:
            current_time = time.time()
            if current_time - last_request_time[email] < 60:
                return jsonify(
                    {"success": False, 'message': 'Please wait 60 seconds before requesting another captcha'}), 403
        code = random.randint(100000, 999999)
        # 发送验证码到邮箱
        email_captcha.send_email(email, code)

        # 更新用户最近一次请求验证码的时间
        last_request_time[email] = time.time()

        return jsonify({"success": True, 'message': 'Captcha sent successfully'})
    else:
        return 'Forbidden', 400


@app.route('/forget', methods=['POST', 'GET'])
def api_forget():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        input_code = data.get('vercode')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        if email and input_code and password and confirmPassword:
            if email_captcha.verify_code(email, input_code):
                if password == confirmPassword:
                    if mysqldb.user_forget(email, password):
                        return jsonify({"success": True, 'message': '密码修改成功'})
                    elif mysqldb.user_forget(email, password) == 'user_not_exist':
                        return jsonify({"success": False, 'message': '用户不存在', 'code': 1404})
                else:
                    return jsonify({"success": False, 'message': '两次密码不一致'})
            else:
                return jsonify({"success": False, 'message': '验证码错误'})
        else:
            return jsonify({"success": True, 'message': '密码修改成功'})
    elif request.method == 'GET':
        return render_template('forget.html')


@app.route('/create', methods=['POST', 'GET'])
@rate_limited
def user_create():
    if request.method == 'POST':
        data_message = request.get_json()
        print(data_message)
        username = data_message['username']
        grade = data_message['grade']
        grade_class = data_message['class']
        message = data_message['message']
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        broswer = request.headers.get('User-Agent')
        if mysqldb.add_message(username, ip, broswer, message, grade, grade_class):
            return jsonify({"success": True, 'code': 200})
        else:
            return jsonify({"success": False, 'code': 250})
    elif request.method == 'GET':
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return render_template('create.html', ip=ip)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
