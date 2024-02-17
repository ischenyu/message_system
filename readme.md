<h1 align="center">My votes</h1>
<p1 align="center">一个简单、可以自托管的投票系统</p1>

## 项目介绍
本项目使用flask作为后端框架，MySQL作为数据库，redis作为缓存，使用python3.9开发，支持linux、mac、windows环境。

## 项目功能
### 已完成
- [x] 用户注册
- [x] 发送验证码并校验
- [x] 用户登录
- [x] 查询用户信息
### 待办
- [ ] 生成图形验证码
- [ ] 接入Google reCAPTCHA v2
- [ ] 投票创建、进行逻辑及界面
- [ ] 投票列表
- [ ] 投票详情
- [ ] 网站后台管理

## 项目demo
会于2024年2月18日 下午3:00之前部署到 https://myvotes.alistnas.xyz/
## 项目部署
先将sql.sql导入到MySQL数据库中，然后在根目录下执行:
```bash
git clone https://github.com/ischenyu/myvotes
cd myvotes
pip install -r requirements.txt
python app.py
```