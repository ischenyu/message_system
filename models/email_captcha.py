# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
# 用于构建邮件头
# 发信方的信息：发信邮箱，126 邮箱授权码
from_addr = 'abb1234aabb@163.com'
password = 'ENWHVUCJXFARZRBA'

# 发信服务器
smtp_server = 'smtp.163.com'
global code

def send(email, code):
    code = code
    to_addr = email
    """标题"""
    head = "Paimon-邮箱验证码"
    """正文"""
    text = f"您的验证码{code},该验证码5分钟内有效,请勿泄漏于他人！"
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(text, 'plain', 'utf-8')

    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(head)

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    return '{"success":"true"}'


def verify_code(email, input_code):
    import threading
    
    # 使用字典存储用户邮箱和对应的验证码
    user_verification_codes = {}
    
    # 使用锁确保对共享数据的安全访问
    lock = threading.Lock()
    
    with lock:
        if email in user_verification_codes:
            if int(input_code) == int(user_verification_codes[email]):
                del user_verification_codes[email]
                return True
            else:
                return False
        else:
            # 邮箱地址不存在时返回特定状态（例如：-1）
            return -1
