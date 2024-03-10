import smtplib
import threading
from email.mime.text import MIMEText

from_addr = 'abb1234aabb@163.com'
smtp_server = 'smtp.163.com'
password = 'ENWHVUCJXFARZRBA'

user_verification_codes = {}
lock = threading.Lock()

class VerificationError(Exception):
    pass

# 修改 send_email 函数以生成并存储验证码
def send_email(email, code):

    user_verification_codes[email] = code  # 将验证码与邮箱关联存储
    
    text = f"您的验证码{code}, 该验证码5分钟内有效，请勿泄露给他人！"
    
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = email
    msg['Subject'] = "Paimon-邮箱验证码"
    
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.login(from_addr, password)
        server.sendmail(from_addr, [email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

# 在 verify_code 函数中验证用户输入的验证码
def verify_code(email, input_code):
    with lock:
        stored_code = user_verification_codes.get(email)
        if stored_code is None:
            raise VerificationError("找不到对应邮箱的验证码")
        
        if int(input_code) == int(stored_code):
            # 需要注意，传入的验证码是字符串，所以需要转换为整数进行比较
            del user_verification_codes[email]
            return True
        else:
            raise VerificationError("输入的验证码与存储的不匹配")