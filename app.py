import random
import time

from flask import Flask, make_response, render_template, request, jsonify, redirect, url_for, redirect
from itsdangerous import URLSafeSerializer

from models import email_captcha
from models import mysqldb

app = Flask(__name__, static_folder='static')
app.secret_key = 'cookie_key'  # 设置一个用于签名的秘钥
# 创建一个序列化器对象
serializer = URLSafeSerializer(app.secret_key)


@app.route("/")
def index():
    try:
        logining = request.cookies.get('logining')
        user_email = request.cookies.get('user_email')
        if logining == 'True':
            return render_template("index.html", logined=True, email=user_email)
        else:
            return render_template("index.html")
    except AttributeError:
        return render_template("index.html")

@app.route('/login')
def login():
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

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/forget')
def forget():
    return render_template("forget.html")

@app.route('/api/user/register', methods=['POST', 'GET'])
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
                    if mysqldb.User_signup(username, password, email):
                        return jsonify({"code": 200, "success": True, "message": "注册成功"})
                    elif mysqldb.User_signup(username, password, email) == 114:
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
    else:
        return "这是api接口,你给我爬啊", 403

@app.route('/api/user/login', methods=['POST', 'GET'])
def api_login():
    if request.method == 'POST':
        try:
            # 获取传回的数据
            data = request.get_json()
            username = data['username']
            email = data['username']
            password = data['password']
            if mysqldb.User_login(username, password):
                # 用户信息写入数据库，注册成功后写入cookie，重定向到主页.
                max_age = 604800
                # 加密用户信息并设置到 Cookie 中
                encrypted_email = serializer.dumps(email)
                resp = make_response(jsonify({"success": True, "message": "登录成功", 'code': 200}))
                resp.set_cookie('user_email', encrypted_email, max_age=max_age)
                resp.set_cookie('logining', str(True), max_age=max_age)
                return resp
            elif mysqldb.User_login(username, password) == 'error':
                return jsonify({"message": "服务器内部错误"}), 500
            else:
                return jsonify({"code": 401, "message": "用户名或密码错误"}), 401
        except KeyError:
            return jsonify({"code": 400, "message": "回调数据不完整！"}), 400
    else:
        return "这是api接口,你给我爬啊", 403

# 记录用户最近一次请求验证码的时间
last_request_time = {}

@app.route('/api/user/register/captcha', methods=['POST', 'GET'])
def captcha():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        print(email)
        if not email:
            return jsonify({"success": False, 'message': 'Email is required'}), 400

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

@app.route('/api/user/forget', methods=['POST', 'GET'])
def api_forget():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        input_code = data.get('vercode')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        if email and input_code and password and confirmPassword:
            if email_captcha.verify_code(email, input_code) == True:
                if password == confirmPassword:
                    if mysqldb.User_forget(email, password) == True:
                        return jsonify({"success": True, 'message': '密码修改成功'})
                    else:
                        return jsonify({"success": False, 'message': '密码修改失败'})
                else:
                    return jsonify({"success": False, 'message': '两次密码不一致'})
            else:
                return jsonify({"success": False, 'message': '验证码错误'})
        else:
            return jsonify({"success": True, 'message': '密码修改成功'})

@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == "__main__":
    # 933d9673cc
    app.run(debug=True)
