# AI 智能客服平台 (从零可运行 Demo)

这个项目是一个完整的 AI 客服 MVP，包含：

- FastAPI 后端接口
- SQLite 数据库存储问答与聊天记录
- 基于 Sentence-Transformers 的语义检索问答
- 微调脚本 (fine-tune)
- 在线免费问答数据导入 (StackExchange API)
- 可直接访问的前端 UI 管理与聊天页面

## 1. 项目结构

- backend: 后端服务与数据库模型
- frontend: 聊天与管理 UI
- scripts: 初始化、导入、微调脚本
- data/sample_qa.csv: 本地演示问答数据
- run_demo.ps1: 一键运行演示

## 2. 环境要求

- Python 3.10+
- Windows PowerShell
- 可联网下载模型与依赖

## 3. 一键 Demo

在项目根目录执行：

```powershell
.\run_demo.ps1
```

脚本会自动：

1. 创建虚拟环境并安装依赖
2. 初始化 SQLite 数据库
3. 导入本地问答样例
4. 抓取在线免费问答数据
5. 微调语义模型
6. 启动服务

启动后访问：

- 前端 UI: http://127.0.0.1:8000
- 健康检查: http://127.0.0.1:8000/health
- API 文档: http://127.0.0.1:8000/docs

## 4. 分步运行命令

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python scripts/init_db.py
python scripts/seed_from_csv.py --file data/sample_qa.csv
python scripts/import_online_qa.py --tag python --limit 30
python scripts/fine_tune_encoder.py --epochs 1 --batch-size 8

uvicorn backend.main:app --reload
```

## 5. CSV 导入格式

CSV 列名必须包含：

- question
- answer
- source (可选)

示例见 data/sample_qa.csv。

## 6. 说明

- 若未微调成功，系统会自动回退到基础开源模型进行问答。
- 当前问答策略是语义相似度检索，适合 FAQ/客服知识库场景。
- 你可以继续扩展：用户登录、工单流转、人工坐席接管、RAG 文档检索等。
