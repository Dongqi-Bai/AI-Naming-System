# 字里 · AI 起名系统

一个基于 FastAPI 与 Vue 3 的前后端分离 AI 起名系统，包含登录、注册和 AI 起名三个页面。

## 功能

- 邮箱验证码注册
- 密码哈希存储
- JWT 登录与登录状态校验
- 受保护的 AI 起名接口
- 按姓氏、性别、字数、偏好和避用字生成名字
- 响应式页面，适配桌面端与移动端

## 项目结构

```text
backend/     FastAPI、SQLAlchemy、AI 服务与认证逻辑
frontend/    Vue 3、Vue Router 与页面样式
```

## 本地启动

### 1. 配置后端

复制 `.env.example` 为 `.env`，至少填写以下内容：

```env
JWT_SECRET_KEY=一段足够长的随机字符串
MAIL_USERNAME=你的发件邮箱
MAIL_PASSWORD=邮箱 SMTP 授权码
MAIL_FROM=你的发件邮箱
DEEPSEEK_API_KEY=你的 DeepSeek API Key
```

默认使用项目目录下的 SQLite 数据库。如需使用 MySQL，可以设置：

```env
DB_URI=mysql+aiomysql://用户名:密码@127.0.0.1:3306/数据库名?charset=utf8mb4
```

部署到其他域名时，请通过 `CORS_ORIGINS` 添加前端地址，多个地址使用英文逗号分隔。

安装依赖并启动：

```bash
pip install -r requirements.txt
fastapi dev backend/main.py
```

后端默认地址为 `http://127.0.0.1:8000`，接口文档位于
`http://127.0.0.1:8000/docs`。

### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

浏览器打开 `http://localhost:5173`。开发环境已通过 Vite 将 `/api`
请求代理到本地 FastAPI 服务。

生产环境可在 `frontend/.env.production` 中设置：

```env
VITE_API_BASE_URL=https://你的后端域名
```

## 主要接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/auth/code?email=...` | 发送注册验证码 |
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 用户登录并返回 JWT |
| GET | `/auth/me` | 获取当前登录用户 |
| POST | `/name` | 生成名字，需要 Bearer Token |
