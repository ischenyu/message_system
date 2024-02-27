from flask import Flask, render_template, request, jsonify
from models import email_captcha
import random, time
# from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import mysqldb

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")

from flask import jsonify

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
                if email_captcha.verify_code(email, input_code) == True:
                    if mysqldb.User_signup(username, password, email) == True:
                        return jsonify({"code": 200,"success":True, "message": "注册成功"})
                        # ToDo：用户信息写入数据库，注册成功后重定向到登录页面
                    else:
                        return jsonify({"code":500,"success":False, "message": "注册失败,数据库错误,请联系管理员解决"}),401
                else:
                    return jsonify({"message": "验证码错误"}),401
            except NameError as e:
                print(e)
                return jsonify({"success":False, "message": "验证码错误NameError"})
            except Exception as e:
                print(e)
                return jsonify({"success":False, "message": "验证码错误Exception"})
        else:
            return jsonify({"success":False, "message": "请同意协议"}),400
    else:
        return "这是api接口,你给我爬啊", 403
    
@app.route('/api/user/login', methods=['POST', 'GET'])
def api_login():
    if request.method == 'POST':
        try:
            # 获取传回的数据
            data = request.get_json()
            username = data['username']
            password = data['password']
            if mysqldb.User_login(username, password) == True:
                return jsonify({"success":True, "message": "登录成功", 'code':200})
                # ToDo：用户信息写入数据库，注册成功后写入cookie，重定向到主页
            elif mysqldb.User_login(username, password) == 'error':
                return jsonify({"message": "服务器内部错误"}),500
            else:
                return jsonify({"code": 401, "message": "用户名或密码错误"}),401
        except KeyError:
            return jsonify({"code": 400, "message": "回调数据不完整！"}),400
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
                return jsonify({"success": False, 'message': 'Please wait 60 seconds before requesting another captcha'}), 403
        code = random.randint(000000, 999999)
        # 发送验证码到邮箱
        email_captcha.send_email(email, code)

        # 更新用户最近一次请求验证码的时间
        last_request_time[email] = time.time()

        return jsonify({"success": True, 'message': 'Captcha sent successfully'})
    else:
        return 'Forbidden', 400


if __name__ == "__main__":
    # 933d9673cc
    app.run(debug=True)