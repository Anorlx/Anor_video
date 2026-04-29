# Anor Video

Anor Video 是一个视频链接解析、下载与 AI 总结问答项目。项目只包含前端和后端源码，未包含本地数据库、下载缓存、构建产物或任何真实密钥。

## 项目结构

```text
.
├── backend/   # FastAPI 后端服务
└── frontend/  # Vue + Vite 前端应用
```

## 后端启动

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload --host 0.0.0.0 --port 8010
```

启动前请在 `backend/.env` 中填写自己的 API Key、JWT 密钥和支付配置。不要把 `.env` 提交到 GitHub。

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

默认前端会连接本地后端服务。生产部署时请按自己的域名和后端地址配置环境变量或代理。

## 安全说明

- 本仓库不包含 `.env`、本地 SQLite 数据库、下载文件、日志、`node_modules` 或前端构建目录。
- `backend/.env.example` 只保留占位符，用于说明需要配置哪些变量。
- 线上部署前请使用强随机字符串配置 `JWT_SECRET`，并在服务端环境变量中保存真实密钥。
