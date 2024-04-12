<h1 align="center">留言系统</h1>

## 项目介绍
本项目使用flask作为后端框架，MySQL作为数据库，redis作为缓存，使用python3.9开发，支持linux、mac、windows环境。

## 项目功能
### 已完成
- [x] 用户注册
- [x] 发送验证码并校验
- [x] 用户登录
- [x] 查询用户信息
- [x] 接入Google reCaptcha
### 待办
- [ ] 留言记录显示
- [ ] 网站后台管理

## 项目demo
https://message.alistnas.top/
## 项目部署
先将sql.sql导入到MySQL数据库中，然后在根目录下执行:
```bash
git clone https://github.com/ischenyu/message_system.git
cd message_system
pip install -r requirements.txt
python app.py
```